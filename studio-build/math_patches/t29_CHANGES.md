# Topic 29 — Probability: changes (course review 2026-09)

Patch: `math_patches/t29.py`. Check: `python3 math_check.py 29` → 0 problems, 0 warnings, 0 layout problems.
Guided questions are renumbered automatically in course order (new ones become Q12–Q15 and Q22).

## 1. Wrong rules fixed
- **"OR → add"** (lesson "And · Or"): the board now says "OR → add the **separate** cases". The teacher adds a
  two-or-five example and warns that overlapping cases get counted twice.
- **New slide "OR with overlap"** (same video): numbers 1 to 30 divisible by 4 or 6: 7 + 5 − 2 = 10 → 1/3.
  OR = first + second − both (linked to Overlapping groups). Also adds a size check: AND → smaller, OR → bigger.
- **Q7 / Q9 videos:** "dependent choice" (these dice are independent) → "forced choice: only one number works".
- **Q8 video:** "Seven heads in a row" → "Six heads already — a seventh head in a row?".
- **Q12 (now Q16) video:** the story example "picks seven, another picks nine" (not symmetric) → "five and nine".
- **Dice symmetry slide:** removed the off-topic remark about opposite faces. Added the real reason (swap each face
  x for 7 − x, so a sum of 9 becomes a sum of 5) and the rule "two n-sided dice → most likely sum is n + 1" (for p05).

## 2. Methods added
- **Lesson "Possible first"**: "possible = the group they choose FROM" (40 students, 18 in music → bottom 18). Covers p26.
- **New lesson video `r26-t29-more-rules`** (after Q11, ~2.9 min, same sidebar as the other lesson parts):
  - At least one = 1 − none (two dice, at least one six = 11/36, and the 12/36 trap).
  - Exactly one = RB + BR; exactly k = one order × number of orders (3 tosses, exactly 1 head = 3/8);
    "drawn together" = one after the other, without replacement.
  - Two stages: a **tree** (SVG tree on the slide): multiply along a branch, add the branches; the "pour the
    bags together" trap.
  - Unknown count in the bag (5/(5 + x) = 1/3), and working back from the answers.
- **Four new guided questions with solution videos** (Q12–Q15):
  - Q12 `q-r26-t29-01` OR with overlap (story: soccer/chess class) — add − overlap, plus a Venn-diagram check.
  - Q13 `q-r26-t29-02` at least one (guessing 3 quiz questions): 1 − (3/4)³ = 37/64; traps 27/64 and 3/4.
  - Q14 `q-r26-t29-03` two boxes and a coin (tree): 23/40; trap 5/9 (pouring the boxes together).
  - Q15 `q-r26-t29-04` how many red marbles to add so P = 3/4: equation, then working back from the answers.
- **Q11 video** reordered for weak students: simple way first (2 lockers out of 7), then the two separate cases as a
  check. The complement method moved to the new "At least one" slide.
- **Q10 video:** one line added: "drawn together = one after the other, without replacement".
- **Recap slide** updated (at least one, OR minus overlap, tree).

## 3. Geometric probability (missing from the whole course) — new
- **New lesson video `r26-t29-geometric`** (end of "Further guided examples", ~1.9 min): area over area (a 4 × 5
  rectangle in a 10 × 10 square → 1/5); the three areas needed (rectangle, triangle, circle); a circle in a square = π/4;
  a triangle on a side of a rectangle = always 1/2. Figures are SVG in the geometry style.
- **Guided Q22** `q-r26-t29-05` (with a figure): square of side 6, circle of radius 2, P(shaded) = 1 − π/9. The
  solution video goes through the traps: the circle instead of the shaded region, a radius that was not squared, and
  comparing lengths instead of areas.
- **3 practice questions with figures:** triangle in an 8 × 5 rectangle (1/2), round target of radius 10 with a
  radius-2 circle in the center (1/25, trap 1/5), and working backward: P = 0.36 → x = 6 (trap 3.6).
- **New memory card** "Geometric probability".
- **Teacher decision:** the review suggests this could go in geometry (T32–T33 or T38), because circle area is taught
  there. I put it in T29, where the probability idea lives, and the lesson reminds students of the three area
  formulas it needs. To move the whole block, add `M.move()` calls for `r26-t29-geometric`, `q-r26-t29-05`,
  its solution video and `mem-r26-t29-geometric` into a geometry section (and move practice q-r26-t29-12/13/14).

## 4. Text
- Every guided and practice solution was rewritten: numbers in TeX, possible first, the method the lesson teaches
  (faster method after it), traps named. There is no mid-sentence "so" and no "2:14 = one seventh" left.
- Stems: removed stray spaces and "uniformly (random)" wording ("at random"). Letters are in TeX ($r$, $s$, $A$, $B$).
  Clearer stems for g150, g152–g154, g157, g160–g165, p04, p07, p09–p12, p14–p19, p22, p24, p25.
  "Which statement is true" → "Which of the following is correct?". The singular "dice" in stems was kept (NITE usage).
- American spelling in all topic videos (color, practice, neighboring, math).
- Memory card "Probability — rules to know": fixed OR row (separate cases / overlap). New rows: sub-group, at least
  one, exactly k, tree, unknown count. New tips: n + 1, the size check, "drawn together", and 7 − x symmetry.

## 5. Practice (27 → 34)
- Removed the near-duplicates p03 (= Q9) and p20 (= Q14 with new letters).
- Added 9 questions: unknown count ×2 (q-06, q-07), raffle "at least one", drawn together (q-08), tree / rain-walk
  (q-09), overlap from "neither" (q-10), committee "both chosen", two ways (q-11), geometric ×3 (q-12 to q-14).
- Reordered easy → hard. The hardest items (p17, committee q-11, p13, p16) come last.

## Counts
Questions rewritten: 42 (all remaining guided + practice). Added: 14 (5 guided, 9 practice). Removed: 2.
Slides changed: 14. Slides added: 1 (OR with overlap), plus 17 slides in new videos. Videos added: 7 (2 lessons, 5 solutions).
Figures: 4 question figures and 4 slide figures (3 geometry figures and the tree). Memory cards: 1 updated, 1 new.

## API workarounds
- There is no "append to slide" call. The patch rebuilds the old script from its lines (`_script_of`) and adds lines to it.
- The sidebars for the solution videos list the pre-renumbering numbers in course order, so `renumber_guided()` can
  sort them into Q1–Q16 (learn) and Q17–Q22 (advanced).

## Pass 2 (teacher-approved remove/restore plan + summary lesson)
**Removed (plan):**
- The whole geometric probability block: lesson video `r26-t29-geometric` (5 slides, 3 figures), guided
  `q-r26-t29-05` (+ figure) and `solve-q-r26-t29-05`, the card `mem-r26-t29-geometric`, and the practice items
  `q-r26-t29-12`, `-13`, `-14` (with their figures). "Question 22" is gone from the advanced sidebar.
- "Unknown count": the slide in `r26-t29-more-rules` (and its sidebar entry in all lesson parts), guided `q-r26-t29-04`
  + `solve-q-r26-t29-04`, practice `q-r26-t29-06` and `-07`, and the card row. The more-rules title slide now says
  "Three more tools".
- The AND/OR size check: the last board item and two lines of the "OR with overlap" slide, and the card tip.

**Restored (plan):**
- Practice **wp29-p03** (two eight-sided dice match: 1/8) and **wp29-p20** (k boxes, cards 1 to m: 1/m^k), with text
  clean-up only (TeX letters, "at random", worked numbers; p20 has a plug-in check k = 2, m = 3).
- Dice symmetry slide: "By the way — opposite faces of a die always add to seven…" is back (the 7 − x reason stays after it).
- "And · Or" slide: the original lines 'By the way — "or" questions are much rarer on the exam. They're also the
  harder ones.' and 'Most of what you'll see is "and".' (the separate-cases condition stays).
- Card: the original OR example 1/7 + 6/7 · 1/6 = 2/7 next to the new one, and the full tip '"Or" questions are rare —
  and a second try only happens after a first miss.'
- Q11 video (`solve-wp29-g158`): the original complement slide is back as slide 4, "Method 3 · Complement" (miss both:
  6/7 · 5/6 = 5/7 → 1 − 5/7 = 2/7). Its last line ("two lockers cover two of the seven places") is not repeated,
  because it is now Method 1.

Guided questions renumber automatically: the three new learn-section questions are Q12–Q14, g160 is Q15, the
advanced ones are Q16–Q20. Practice: 34 → 31 (−5 removed, +2 restored), still easy → hard.

**New: summary video `r26-t29-summary` "Summary: Probability"** (about 3.4 min), at the end of "Further guided examples",
right before the practice. Slides: Summary · Wanted over possible · Possible first · The complement · AND · OR ·
At least one · exactly one · Two stages: a tree · Shortcuts · Before you practice (checks: what is possible — everyone
or a smaller group; AND or OR; can the OR cases happen together; "at least one" → 1 − none; did the bag change; traps:
adding instead of 1 − none, pouring two bags together, giving the complement instead of what was asked).

**For the teacher:** the Q13 video still says "Size check: with five questions, that way gives five quarters — more
than one. Impossible." This is the "a probability can't be more than 1" check, not the removed AND/OR size check, so it stays.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). A lesson slide is cut only where a question video in the same section teaches the same idea; ideas no question teaches stay. Nothing in topic 29 is recorded. Questions, numbers, methods and the memory card are unchanged.
- **`r26-t29-more-rules`** (the flagged "More Rules" lesson): 4 → 2 slides, 2.4 → 1.0 min. Title slide renamed "Exactly One"; new lines: "More tools for the harder exam questions. One of them here: exactly one. The others — OR with overlap, at least one, and two stages — we learn in the questions." Cut: "At least one" (1 − none, two dice, the 1/6 + 1/6 trap) → Q13 `solve-q-r26-t29-02` (1 − none, the adding trap, the "none" trap); "Two stages: a tree" (bags A/B, multiply along a branch, add branches, don't pour the bags) → Q14 `solve-q-r26-t29-03` (same tree, same pour trap). KEPT "Exactly one" (RB + BR, exactly k = one order × number of orders, HTT example): no question video teaches it. Only its last line + board item "Drawn together = one after the other, without replacement" was cut — Q10 `solve-wp29-g157` already teaches it; it now ends "Let's see the other tools in the questions."
- **`wp-151` And · Or**: 3 → 2 slides, 1.5 → 1.0 min. Cut "OR with overlap" (1–30 divisible by 4 or 6) → Q12 `solve-q-r26-t29-01` (soccer or chess: counted twice, subtract once, two circles). MOVED its rule as a board item into Q12 slide 2: "OR = first + second − both" (appears at "Subtract them once"). "That's the next slide." → "We'll see that in a question soon."
- **`wp-159` Dice symmetry**: 3 → 2 slides, 2.0 → 1.9 min. Cut the Recap slide (the memory card and the summary video keep it); its last line "Next question — the symmetry in action." moved to the end of the symmetry slide. KEPT the whole symmetry slide (table, 7 − x reason, n faces → n + 1): Q15 only uses "same distance from 7".
- Unchanged: `wp-146` (wanted over possible, 0–1, possible first, smaller group — the long Hebrew intro) and `wp-147-after` (certain & impossible): no question video repeats them.
- Shared lesson sidebar (all five lesson parts) is now: Wanted over possible · Between 0 and 1 · Possible first · Certain & impossible · And · Or · Exactly one · Dice symmetry ("OR with overlap", "At least one", "Two stages: a tree", "Recap" removed; active slides renumbered).
- **Net: −2.0 min.** No video said "as we saw in the lesson" about a cut idea. The summary video `r26-t29-summary` was not edited; everything it recaps is still taught (lesson slides kept, or Q12–Q14).
- **Follow-up (re-audit of every cut idea):** every cut idea now names the video that teaches it. "At least one" → Q13 (1 − none, the adding trap); "Two stages: a tree" → Q14; "Drawn together" → Q10; "OR = first + second − both" → Q12; the Recap's items → kept lesson slides, the complement in `solve-wp29-g150` and Q13 (1 − none), Q12–Q14, and the dice-symmetry slide. One idea had disappeared: on the cut "OR with overlap" slide, students found the overlap themselves (1–30 divisible by 4 or 6 → 12 and 24 are on both lists). That idea is now MOVED to the end of Q12 `solve-q-r26-t29-01` slide 3 as "Sometimes you find the overlap yourself. From one to thirty, divisible by four or by six: twelve and twenty-four are on both lists." + board "1–30, by 4 or by 6: 7 + 5 − 2 = 10". Q12 is 0.1 min longer; topic net is now −1.9 min.

## 2026-10-06 new exam methods
Function `add_methods` (runs last). Nothing in topic 29 is recorded. Check: `python3 math_check.py 29 32` → 0 problems, 0 warnings, 0 layout problems.
- **Card `mem-probability`**: new first table "Which door? Decide first" — COUNT (equally likely outcomes you can list → wanted ÷ all; two dice sum 7 → 6/36 = 1/6), PATH (story in steps → multiply along the path, add the paths; 3 red 2 blue, 2 red in a row → 3/5 · 2/4 = 3/10), SYMMETRY (nobody special → 1/n; 5 people in a random line, Dana last → 1/5).
- **Summary `r26-t29-summary`**: new slide "Which door?" right before "Before you practice" (sidebar entry added; 3.6 → 4.4 min). The three doors with the same three examples, one board line + one example line each. Covers 17 of the 24 real probability questions.

## 2026-10-06 practice: new methods
Function `practice_methods` (runs last in `apply`). One extra line is added at the end of each written solution, starting with a "Door:" tag; the existing lines are kept. Lines were added only where the door gives a second route or explains a trap, not where they would only repeat the solution. Nothing is recorded.
- `q-r26-t29-11` (Dana and Tal both on a committee of 3 of 10): Door: SYMMETRY — 3 of the 45 pairs → 1/15.
- `wp29-p22` (two tokens, different colors): Door: COUNT — 20 mixed pairs of 36 → 5/9.
- `q-r26-t29-08` (at least one winning ticket): Door: COUNT — 10 pairs, 3 with no winner → 7/10.
- `wp29-p21` (at least one six with two dice): Door: COUNT — 6 + 6 − 1 = 11 of 36.
- `wp29-p10` (choose a bag, then a token): Door: PATH, not COUNT — tokens in A have 1/24, in B 1/20, so pouring the bags together (5/11) is wrong.
- `wp29-p16` (coin sum greater than the dice): Door: COUNT — 64 equally likely outcomes, 3 + 2 good → 5/64.
- Every line checked in python (p16 by listing all 64 outcomes). Check: `math_check.py 29 32` → 0 / 0 / 0.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has new numbers and a new story.
The idea, the trap, the level and the methods stay the same (possible first, complement, AND → multiply, a first stage
that can't go wrong, the forced second die, separate OR cases + complement, symmetry around 7, plug-in with distinct
choices, the jante symmetry flash). Every guided solution video was rewritten to match (speech, draw cues, the dice grids,
slide titles where they name objects, video titles / pre-loaded text). Function `renumber_pass(M)` runs last, after
`cut_repeats`, `add_methods` and `practice_methods`. The door lines that `practice_methods` added are rewritten with the new
numbers (p10 PATH, p16 COUNT). p17's "by symmetry" line is now tagged "Door: SYMMETRY" because q-11 (the only other one) is
gone. Nothing in topic 29 is recorded.

**Dice are 6-sided (teacher rule):** the old English used 8-sided dice in g147, g152, g156, p03, p05, p13 and p16. Where a
6-sided die would land back on the Hebrew numbers, the item now uses a spinner with equal sections or numbered cards.
The "n faces → top sum n + 1" rule (lesson wp-159, card tip, summary Shortcuts) became "one card from each of two sets
numbered 1 to n → top sum n + 1".

**Counts:** 17 guided questions renumbered, with 17 solution videos rewritten. 19 practice questions renumbered.
Lesson / summary / card examples changed: the wp-159 n-sided-dice lines; in the summary, "four heads in a row" → five,
"heads and a three = 1/12" (the Hebrew lesson example) → "tails and a number above four = 1/6", "second try 1/5 + 4/5 · 1/4"
(the Hebrew five doors) → "1/6 + 5/6 · 1/5 = 1/3", and "ten and four" (the Hebrew) → "eleven and three"; g150's "pass 2/3, fail
1/3" (the Hebrew) → 3/4 and 1/4; and 6 example cells on the memory card that copied the questions or the Hebrew.
**Practice 31 → 24.**

**Practice clean-up:** copy removed: p03 (= guided g156). English extras: kept 3 (p22 two colors drawn together, p23 exactly
two heads, p25 exactly one red). Removed p21 (= the card example), p24 (= the board example in guided q-01's video), p26
(= the lesson example "40 students, 18 music"), and p27 (at least one, already drilled in q-08 and guided q-02). September items:
kept q-08 (at least one) and q-10 (overlap from "neither"), because the Hebrew practice has neither type. Removed q-09
(a tree, already in p10 / p15) and q-11 (both chosen, already in p17). Order: easy → hard.

**Kept on purpose:** the English-made guided q-r26-t29-01 to 03 and the lessons' own English examples. p08 keeps four tosses
(only the pattern changed, so the answer is still 1/16). Its type and length stay the same, because changing the number of
tosses would change the question. The guided order is unchanged (it already goes easy → hard). The correct-answer position
moved in 15 of 17 guided questions.

**Checks:** every answer was enumerated exactly in Python with fractions (dice / coin / spinner product spaces, all 8!
candy orders, all 12·11 counter pairs, all 6! prize assignments, the device over 16², the day-by-day chains). Every video step and
method was recomputed: g158 by all three methods, the g162 plug-ins (1, 1 → all 1; 2, 2 → three choices = 1/4; 3, 2 → 3/2,
1/9, 1/8, 1/6 all different), and p20 with k = 3, t = 4 (all different). The traps are still among the choices: wanted = 1 (1/11,
1/10), complement / red count (16, 1/12, 2/25), adding instead of multiplying (7/10), unordered pairs (1/18), 1/8 + 1/7 =
15/56, the first step only (2/7), pouring the bags (9/17), sum 7 for card sums, and averaging the two farm rates (43/48).
The new numbers were checked against the Hebrew subtitles: none land on a Hebrew number, object or day (Sunday → Tuesday,
the 22 letters, the 5 doors, 4 desserts, etc.). Duplicate scan over topics 1–29 (questions, lesson lines, boards):
no question equals another question or a lesson / card example. `python3 math_check.py 29 32` → PROBLEMS 0, WARNINGS 0,
LAYOUT 0. Rendered g150, g154, g156, g161, g162, g165, wp-159 and the summary and looked at them (the 6×6 grid highlights
sum 5 and the 5×5 grid its diagonal; both grids were moved so they no longer touch the stem or label). No "Question N" was added
to spoken lines.

| id | old (English base, Hebrew-derived) | new | answer |
|---|---|---|---|
| wp29-g147 | 8-sided die, even | spinner 10 equal sections, even | 1/2 (2) |
| wp29-g148 | 5 green, 4 orange counters | 7 blue, 4 white marbles | 7/11 (3) |
| wp29-g149 | 8 purple 5 white, 3 purple out | 11 orange 7 white, 4 orange out | 1/2 (1) |
| wp29-g150 | 28 tokens, gold 3/7 → silver | 36 tokens, red 4/9 → blue | 20 (4) |
| wp29-g152 | coin + 8-sided die: heads and 5 | coin + spinner 1–5: tails and 4 | 1/10 (3) |
| wp29-g153 | 4 tosses all tails | 5 tosses all tails | 1/32 (2) |
| wp29-g154 | two dice, sum 8 | two dice, sum 5 (first die 4/6, then 1/6) | 1/9 (3) |
| wp29-g155 | Rosa / Sam, 6 in a row | Omar / Kate, 7 in a row | equal (1) |
| wp29-g156 | two 8-sided dice match | two spinners 1–5 match | 1/5 (2) |
| wp29-g157 | 4 red 4 yellow, different colors | 6 green 6 white | 6/11 (3) |
| wp29-g158 | prize in 7 lockers, open 2 | prize in 8 boxes, open 2 | 1/4 (3) |
| wp29-g160 | sums 9 vs 5 | sums 8 vs 6 | A = B (2) |
| wp29-g161 | 26 letters / NOAH | 7 weekdays / 2 weekend days (Ella, Omar) | 1/7 (4) |
| wp29-g162 | r groups of s, oldest; plug 2, 3 | m rounds of n envelopes, prize; plug 3, 2 | n^(−m) (3) |
| wp29-g163 | buttons 800/40 + 400/110 | eggs 600/25 + 300/50 cracked | 11/12 (3) |
| wp29-g164 | 5 genres, Mon jazz → Wed folk | 6 gym classes, Thu yoga → Sat boxing | 4/25 (3) |
| wp29-g165 | 6 red + 1 blue, 5th blue | 7 lemon + 1 mint, 6th mint | 1/8 (2) |
| wp29-p01 | 12 red 8 blue, 1 red out | 15 yellow 9 green, 1 yellow out | 14/23 (2) |
| wp29-p02 | 14 tokens, white = black | 20 balls, red = green | 8 (3) |
| wp29-p04 | bulbs 200/20 + 100/25 | phones 300/20 + 100/12 | 23/25 (4) |
| wp29-p05 | two 8-sided dice, top sum | two boxes of cards 1–10, top sum | 11 (1) |
| wp29-p06 | 30 tokens, 1/5 and 1/3 | 36 tokens, 1/4 and 1/3 | 15 (2) |
| wp29-p07 | 6 each of 3 colors, 4 out | 7 each of 4 colors, 3 out | 4/25 (1) |
| wp29-p08 | die 4×: odd, odd, even, odd | die 4×: even, even, odd, even | 1/16 (3) |
| wp29-p09 | 5 colors, 4 draws all blue | 3 colors, 4 draws all green | 1/81 (2) |
| wp29-p10 | A 8r 4b, B 2r 8b | A 3 white 6 black, B 6 white 2 black | 13/24 (3) |
| wp29-p11 | 4 people, Nina six, others not | 5 friends, Maya a 1, others not | 625/7776 (2) |
| wp29-p12 | socks 4, shoes 3 | cups 6, plates 4 | 1/6 (3) |
| wp29-p13 | 8-sided until 8, exactly 5 rolls | die until 6, exactly 4 tosses | 125/1296 (1) |
| wp29-p14 | 0–11, ±2, first 5 / second not | 0–15, ±3, first 7 / second not | 7/64 (4) |
| wp29-p15 | 4 badges, Mon blue → Wed red | 7 soups, Mon tomato → Wed lentil | 5/36 (3) |
| wp29-p16 | 8-sided die vs 0/1 coin ×3 | 6-sided die vs 0/1 coin ×3 | 5/48 (2) |
| wp29-p17 | 5 gifts 2 books, Ada & Ben | 6 prizes 2 tickets, Noa & Eli | 1/15 (2) |
| wp29-p18 | heads = 2/5 of tails | tails = 3/4 of heads | 3/7 (3) |
| wp29-p19 | coin 2/3, 5 tosses, even | coin 4/7, 6 tosses, even | 1/2 (2) |
| wp29-p20 | k boxes, cards 1–m, all 2 | k bags, balls 1–t, all 1 (plug 3, 4) | 1/t^k (4) |
| lesson wp-159 | two n-faced dice → n + 1 (6 → 7, 8 → 9) | cards 1 to n → n + 1 (1–6 → 7, 1–8 → 9) | – |
| summary | four heads; heads & 3 = 1/12; 1/5 + 4/5·1/4; ten and four; n faces | five heads; tails & above 4 = 1/6; 1/6 + 5/6·1/5 = 1/3; eleven and three; cards 1 to n | – |
| card mem-probability | 5 green 4 orange; gold 3/7; heads & 5 (8-sided); 1/7 + 6/7·1/6; double 1·1/8; 8 → 7 left; 8 faces: 9 | 2 red 5 green; win 3/8; tails & above 4; 1/6 + 5/6·1/5; three coins 1·½·½; 9 → 8 left; cards 1 to 8: 9 | – |

## 2026-10-06 review
Independent review of the renumber pass (built with and without `renumber_pass`, compared every changed question and video).
Checked: 17 guided questions + their videos, 19 renumbered practice questions, the lesson / summary / card changes, the 7
practice removals. Every key was enumerated with exact fractions (one correct choice each; traps still among the choices);
every video step recomputed; type / condition / difficulty match the old versions; nothing in topic 29 is recorded.
Fixed (in `rn_guided`):
- g148: "7 blue, 4 white" landed on the Hebrew's colors (the Hebrew bag had 5 blue and 4 white) → 7 green, 4 yellow marbles
  (question, explanation and video). Answer still 7/11, choice 3.
- g165: the object was still candies (the Hebrew jar of candies) → a hat with 7 blank tickets and 1 prize ticket; the sixth
  ticket drawn is the prize (question, explanation, all spoken lines). Answer still 1/8, choice 2; both methods unchanged.
- g154 / g156: the questions' own `solutionVisual` still held the old grids (sum 8; 8 × 8) → sum 5; 5 × 5 diagonal.
Open: g156's grid label is the renderer's fixed text "Matching faces" (base renderer: `v.diagonal ? 'Matching faces' : …`,
no per-item label), so it stays for the spinners — needs a renderer option, not a t29 change.
`python3 math_check.py 29 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered g156 and g165 and looked.

## 2026-10-07 methods spread
Function `spread_methods(M)` in t29.py runs last (after `spinner_label`). Every guided and practice question was checked
for "which door?" (COUNT / PATH / SYMMETRY) and the other 2026-10-06 methods. Almost every question already shows its door
in the solution (count the pairs, tree, symmetry) or got a "Door:" line on 2026-10-06; those are skipped. No video slide:
the guided videos already show both routes where two exist. Nothing in topic 29 is recorded.
- **Q10 `wp29-g157`** (6 green, 6 white, two drawn, different colors): Shortcut · Which door? COUNT (self-contained, because Q10 comes before the card that names the doors): 66 equally likely pairs, 36 with two colors → 6/11.
Total: 1 written line, no slides. Recorded: none.

## 2026-10-08 Hebrew points restored
Audit only, no change. Every teaching point of the Hebrew lesson for the sections the 2026-10-05 cut shortened is still taught in the current course, at or before the place it is needed.
- Hebrew "several events" lesson: AND → multiply, OR → add, "or" is rare and harder (And · Or lesson); coin and die (Q5); three tosses (Q6); a dice sum with a forced second die (Q7); history and the roulette (Q8, incl. "rare on the exam"); the double, "first pick doesn't matter", and the tip to work out each event on its own (Q9); without replacement (Q10); the doors, "fail first, then succeed", the driving test, rare and hard (Q11). Dice symmetry: the whole Hebrew lesson is on the kept slide (red/blue dice, don't flip 2-2, opposite faces add to 7, symmetry around 7); the "same question, different wording" line is in Q15. The cut slides ("OR with overlap", the recaps) were not in the Hebrew lesson.
