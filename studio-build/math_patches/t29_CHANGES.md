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
