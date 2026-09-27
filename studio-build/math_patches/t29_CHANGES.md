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
