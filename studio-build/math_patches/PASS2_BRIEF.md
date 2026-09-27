# Pass 2 for your topics: apply the approved remove/restore plan, then add summary lessons

Teacher-approved (2026-09-27). Read `math_patches/BRIEF.md` (style, API, checks) and `math_api.py` docstring first.
You edit only `math_patches/tNN.py` for your topics and append a "## Pass 2" section to `math_patches/tNN_CHANGES.md`.

## Part A - apply the plan exactly
Source: `real_exam/PLAN_REMOVE_RESTORE.md` (your topics' sections). Do exactly what it says, nothing more:
- REMOVE the listed added items (questions incl. their solve- videos, slides, card rows/tips, lesson lines) and fix
  what depends on them (recap lines, sidebars, "N guided questions" titles, spoken references to removed questions).
  Easiest is usually to delete the code in tNN.py that adds them; otherwise remove them at the end of apply().
- RESTORE the listed original questions / slides / lines / card rows / answer choices / original question content
  (take the original from `base-v18.html`, i.e. what the base data has before patches - your patch must simply stop
  deleting/overwriting it). Restored items get the same text clean-up as everything else (TeX, no ':' division,
  stacked givens with \begin{cases} and \n, full numeric solutions) but NOT new content. Place moved originals as
  the plan says (use M.move for items that live in another topic's section; the moved-to topic must exist in flow).
- Teacher decision: in T27 also REMOVE the distance-time graphs block (slides "Distance-time graphs" and
  "Two travelers" in r26-t27-graphs, q-r26-t27-07 with its solution video, practice -19 and -20, and the graph table
  on the card; retitle the video if needed).
- Rule reminder: anything from the original course stays; an added item stays only if the plan keeps it.

## Part B - summary lesson(s)
The teacher wants, at the end of each topic's teaching, right before the self-practice, a short SUMMARY lesson video
that quickly reminds the student of everything important the topic taught: the formulas, the methods, the shortcuts,
the traps, and the "always ask yourself ..." checks (example for percentages: the percent formula, the 10% method,
"multiply along the diagonal, divide by what's left", "always ask: what is my 100%? it can change when there are
several stages").
- Content = ONLY what the topic's lessons actually teach after Part A (original + kept additions). Nothing new.
- Placement: immediately before each practice section of the topic (a topic whose flow is learn -> practice ->
  learn -> practice gets two summaries, each covering the teaching since the previous practice). Use
  `M.new_video('r26-tNN-summary', ..., section=<the last learn section before that practice>, after=<its last item>)`.
- Shape: title slide "Summary", then 5-9 concept slides, one idea per slide: the rule/formula on the board
  (A(..., T('$...$'))), 2-4 short spoken lines, a tiny example where it helps, then a final slide
  "Before you practice" with the 3-5 "always ask yourself" checks and the most common traps. About 2-4 minutes.
  Sidebar = the slide titles. Teacher's voice: short, warm, direct.
- If the topic already ends with a recap slide, the summary replaces nothing - keep the recap; the summary is the
  standalone review video right before practice.

## Checks
`python3 math_check.py <your topics>` until 0 problems / 0 warnings / 0 layout problems; render the summary videos
(`SRC=tmp_check/check-<tag>.html python3 render.py tmp_check/<name>.png r26-tNN-summary`) and look at them. Solve any
question you restored or touched. Final message: per topic - removed / restored counts, summary video(s) added
(titles of their slides), anything you could not do.
