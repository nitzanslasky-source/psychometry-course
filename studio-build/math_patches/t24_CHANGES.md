# Topic 24: Overlapping groups (changes)

Source: `student_review/review_t23-24.md` (Topic 24 part) and `PLAN.md`. Patch: `math_patches/t24.py`.
Check: `python3 math_check.py 24` gives 0 problems, 0 warnings and 0 layout problems (70 slides).

## Counts
- Questions rewritten: 23. That is all 8 guided questions and the 15 remaining practice questions. Every written solution now shows the numbers in TeX. Stems are clearer, and spelling is US.
- Questions added: 11. Three are guided questions with solution videos (q-r26-t24-01 to 03). Eight are practice questions (q-r26-t24-04 to 11).
- Questions removed: 2 near-duplicates. **wp24-p04** repeated guided Question 1 (given both, find neither). **wp24-p02** repeated p08 and Question 9 (everyone is in at least one group).
- Topic total: 25 questions before, 34 after. Guided went from 8 to 11 and practice from 17 to 23.
- Slides changed: 12. Slides added: 3 in existing videos plus 1 in the Question 5 video.
- Videos added: 5. There are 2 lessons, "Two-Way Tables" (5 slides) and "Three Groups" (4 slides), plus 3 solution videos.
- Memory cards: `mem-overlap` rewritten. New card `mem-r26-t24-more`, "Two-way tables and three groups".
- Figures: none. The topic has no question figures.

## Priority 1: wrong or misleading rules
- "Overlap Ranges" slide 4: the note said "Write max(8, 7) → 7", but max(8, 7) = 8. It now says "the smaller of 8 and 7 → 7".
- "Overlap Ranges" slide 8 ("Spot the wording", was slide 7) said "'At most' → maximum [overlap], 'at least' → minimum". That rule is wrong for questions about "only" or "neither" (p16, p07). The new board says that "at most" and "at least" refer to **the thing they ask about**, and adds "Ask: to make THIS small, what must the overlap be?" Two examples follow: at least music only → max overlap; at most neither → max overlap. The recap (slide 11) and the memory card are fixed to match.
- Question 9 (wp24-g078, butterflies, was Q8): "photograph **different** butterflies" could be read as "no overlap". It now says "Two researchers photograph butterflies … show 40 different butterflies."
- p13 (three groups): the solution ended with "we still need a construction". It now proves the answer 0 with a full construction: 35 fiction+history, 30 fiction+science, 30 history+science, 5 fiction only.
- The on-screen "Twenty−one" (a math minus inside a word) in the Question 5 video is gone. The stem now uses numerals, and the slide descriptions are regenerated.

## Priority 2: methods added
- **Other regions (range)**: new slide 7 "Other regions" in "Overlap Ranges". Same 12/8/7 example. The overlap is 3 to 7. From it: at least one = A + B − both, 8 to 12 (larger group up to A + B, never more than the total). Neither = total − union, 0 to 4. Music only = A − both, 1 to 5, and its minimum uses the MAXIMUM overlap.
  - Guided: **new Question 6** (q-r26-t24-01, swim but not run, answer 5). It targets the "at least → min overlap" trap: the trap answer 23 is the most, not the least. Its solution video has 2 methods.
  - Practice: q-r26-t24-07 (greatest neither), -10 (greatest "tennis only"), -11 (which could be "at least one"), plus the existing p07 and p16.
  - Question 5's video now starts with the simpler route. Neither = 48 − union, and the union goes from 21 to 32, so neither goes from 16 to 27. The complements method is now Method 2 and the elimination insight is Method 3.
- **Exactly one**: new slide 6 "Exactly one" in "Exact Overlap". It shows the strip (5 + 4 = 9), then the formula A + B − 2·both (10 + 9 − 10 = 9), then union − both. It is also on the recap and the card. Practice: p12, p17, and the new hard q-r26-t24-08 (greatest exactly one = 43).
- **Two-way (2×2) table**: new lesson video `r26-t24-two-way`. It starts with the trap: 20% of the women and 30% of the men can't be added or averaged. Next it fills a table with totals (plug in 100), and then covers "percent of what?", where the words after "of" pick the whole (row, column or all).
  - Guided: **Question 10** (q-r26-t24-02, walkers, 25%). One slide explains each distractor.
  - Practice: q-r26-t24-04 (counts), -05 (percents), -06 (fractions, exam level).
- **Three groups**: new lesson video `r26-t24-three-groups`. It teaches "count who is missing": min in all three = total − (missing A + missing B + missing C), or 0. The same thing in one line is A + B + C − 2·total. It also covers why 0 can happen (the p13 construction) and that the max in all three is the smallest group.
  - Guided: **Question 11** (q-r26-t24-03, phone/laptop/tablet, 25%). Its traps are 55% (two groups only) and 70% (the maximum).
  - Practice: q-r26-t24-09 (answer 15) and the fixed p13.
- **Work in percent** is now a tip on the memory card. p15's solution now contrasts with Question 7: 55% + 45% = 100% alone forces nothing, but "20% do neither" does.
- Weak-student fixes:
  - "Exact Overlap" slide 3 now says that the strip is the circles "unrolled into one line".
  - Question 2's video shows the easier route (through the union) first. The strip is now Method 2.

## Priority 3: text
- All 23 existing questions got solutions with numbers in TeX, with no words-only steps and no "so" meaning "therefore" in mid-sentence.
- Stems that started with number words ("Fourteen cut…", "Forty-eight are round…") now use numerals.
- Stray spaces around 3 stems were removed. p06 now says "All ranges include both ends" once, instead of "(inclusive)" twice. p11 now asks "the range of possible numbers of people who use both".
- US spelling in all topic videos: organiser → organizer, flavours → types, recognise → recognize, torch → flashlight (Question 1 stem and video).
- Question 3 video: the note "15 : 9 = 5 : 3" is now marked as a ratio.
- The titles of all solution videos show the current stems.

## Priority 5: practice
- Order is easy → hard: p17, p14, p12, new-04, p09, p01, p08, p11, p15, new-11, new-07, p16, p03, p06, p07, p10, new-05, new-10, p05, new-08, new-06, new-09, p13.
- 15 or more items are exam level: p03, p05, p06, p07, p10, p11, p13, p15, p16 and new 05 to 11.

## Placement and numbering
- The two new lessons, with Questions 10 and 11 and the new card, come after Question 9 in the second section. That section is renamed "More methods and guided examples".
- New Question 6 sits right after Question 5, so the old Questions 6–8 are now 7–9. Titles, spoken numbers and sidebars were renumbered automatically.

## API workarounds
- Solution-video titles and "on screen" descriptions were rebuilt inside the patch (`tidy`), because `set_q` does not refresh them.

## For the teacher to decide
- The 2×2 table and three groups are separate short lessons, not slides inside "Exact Overlap". Please check that this is the order you want.
- (Pass 2: p02 and p04 are restored - see below.) p17 (easy exactly one) was kept as an easy warm-up.

## Pass 2 (teacher-approved plan, 2026-09-27)
**Removed:** nothing. `q-r26-t24-08` stays ("exactly one" is an original type).

**Restored:** `wp24-p02` (26 art, 19 music, 11 both → 34) and `wp24-p04` (120 hikers, neither → 15), with TeX choices and numeric solutions. They are placed at the easy start of the practice (p02 first, p04 after p14).

**Summary lesson added:** `r26-t24-summary` "Summary: Overlapping Groups" (about 2.8 minutes), at the end of "More methods and guided examples", right before the practice.
Slides: Summary · Four regions (a full group = its only-region + both) · Count each once (A + B − both + neither = total) · Maximum overlap (the smaller group) · Minimum overlap ((A + B) − total, or 0; fractions and percents) · Other regions (union, neither, A only; "at most / at least" of the thing they ask) · The squares method (strip, exactly one = A + B − 2·both) · Two-way tables (plug in 100, rows/columns, "of the ..." is the whole) · Three groups (min = total − the missing ones, A + B + C − 2·total, max = smallest group) · Before you practice (range or exact?, which region?, what overlap makes THIS big or small?, who is the whole?, plus the common traps).

## 2026-10-01 elite comparison
Target: real exam 2023_autumn_q2_20 (every pair of three groups shares a given number → range of all three).
- The rule "Max in all three = the smallest group" stays exactly as taught. It is the ceiling when only the group sizes are known.
- **Lesson "Three Groups" (r26-t24-three-groups): new slide "Pairs given"** after "Can it be zero?". Clubs of 40, 35 and 30; pairs share 12, 9 and 15. Someone in all three is in every pair, so the maximum is the smallest pair overlap: 9 (not 30). The minimum here can be 0 (12 + 9, 12 + 15 and 9 + 15 all fit in the clubs). Recap has a new line; sidebar updated.
- **Card mem-r26-t24-more**: new row "Max in all three, pairs given — the smallest pair overlap — pairs 12, 9, 15 → 9".
- **Summary (r26-t24-summary), slide "Three groups"**: new line "Pairs given? Max in all three = the smallest pair overlap".
- **New practice question q-r26-t24-12** (last in the practice): choir 50, band 45, drama 40; pairs 14, 11, 16; greatest possible number in all three = 11 (choice 2). Traps: 40 (smallest group), 16 (largest pair), 41 (sum of the pairs).
