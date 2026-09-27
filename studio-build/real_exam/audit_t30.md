# Audit T30 – Lines and angles (report only, nothing edited)

Sources: `math_patches/t30_CHANGES.md`, `math_patches/t30.py`, `real_exam/quant_real.md` (regenerated version), the real exam
figures (`~/nite-psychometry/figures/*.png`, read for every lines_angles question), and the pre-patch course `course18.json`
(to check what the original course already tested).

Policy used (brief + coordinator rules):
- A rule/method the ORIGINAL course questions already need is kept (coordinator rule 2), even without a real-exam hit.
- A new question is judged by its type. Type on the real exam → KEEP. Type not on the real exam and not in the original
  course → REMOVE. Type not on the real exam but already tested by original course questions → UNSURE (the type is original
  content, but the fixers added more of it; teacher decides with one global rule).

Real lines_angles questions (13): 2020_autumn_q2_04, 2021_autumn_q1_05, 2023_autumn_q1_10, 2025_autumn_q1_08,
2019_spring_q1_09, 2020_spring_q2_15, 2021_spring_q2_20, 2023_spring_q1_01, 2025_spring_q1_04, 2019_winter_q2_04,
2023_winter_q2_03, 2024_winter_q2_14, 2025_winter_q2_04.

| Addition | Where (video id / slide / question ids) | Class | Verdict | Evidence (real question ids / count) |
|---|---|---|---|---|
| Right angle: "90° only if marked or given" (and the old "dot in the square" line deleted) | geo-001 slide "Right angle"; card mem-lines-angles row "Right angle" | FIX | KEEP the new line, but RESTORE the deleted line (see last section) | Real figures always mark right angles with a square with a dot: 2020_autumn_q2_20, 2024_autumn_q2_02, 2025_autumn_q2_04, 2019_spring_q1_13 |
| "Adjacent angles on a straight line" + warning | geo-001 slide "Adjacent angles", Recap, card | FIX | KEEP | – |
| "72° : 2" → "72° ÷ 2" | geo-001 slide "Angle bisector" | FIX | KEEP | – |
| Slide 1: strong students may skip ahead | geo-001 slide 1 | FIX | KEEP | – |
| Figure fixes: Z slide, vertical-angles slide, Q1 (geo30-g002), foundation p13; new figures for adv p05, adv p10 (adv p05 stem now refers to figure) | geo-001, geo30-g002, geo30-foundation-p13, geo30-advanced-p05/-p10 | FIX | KEEP | – |
| All 36 old solutions rewritten (TeX, stacked givens, spelling) | all geo30-* questions, solution videos | FIX | KEEP | – |
| Segments on a line: AC+BD=AD+BC; equal parts → count the gaps | geo-001 new slide "Segments on a line"; Recap line; card row "Segments on a line" | METHOD | KEEP | Needed by original geo30-advanced-p03, -p09, -p16 (rule 2). Count-the-gaps: 2025_spring_q1_02 (equally spaced points on a line). Overlap rule itself: 0 real |
| Parallel or not? ⊥/∥ to the same line → parallel; equal small angles or small+large=180° → parallel | geo-001 new slide "Parallel or not?"; card row "When are lines parallel?" | METHOD | KEEP | 2024_winter_q2_14 (which lines are parallel from 88°/88°/92°), 2021_spring_q2_20 (42° and 137°: on which side do b, c meet). Also original adv-p02, -p07 |
| "Don't assume": not to scale, parallel only if given/proved | "Parallel or not?", Recap, card row "Not to scale", card tip "cannot be determined" | METHOD | KEEP | 2024_winter_q2_14 (b looks parallel, is not); "cannot be determined" options in 2019_winter_q2_04, 2025_spring_q1_04, 2025_autumn_q1_08 |
| U shape: angles inside a U add to 180° | geo-001 new slide "The U shape"; card row "U shape" | METHOD | KEEP | 2019_winter_q2_04 (γ+β inside a U = 180°), 2021_spring_q2_20 |
| Zig-zag rule: angles pointing left = angles pointing right | solve-geo30-g007 new slide "The zig-zag rule"; card row "Bent line (Z-type bends)"; card tip "parallel line through each bend" | METHOD | KEEP | 2020_spring_q2_15 (A-B-C-D-E-F zig-zag: 80+70 = 30+?), 2023_winter_q2_03 (β = α + 35°) |
| C shape: α+β+x = 360° | solve-geo30-g007 new slide "The C shape"; card row "Bent line (C shape)" | CONTENT | REMOVE | 0 real (all 13 figures checked; no C-shaped bend). Not in the original course |
| "Overlapping angles: add them and subtract the full turn" (named) | solve-geo30-g006 slide 4 (new spoken line); card tip | METHOD | KEEP | 2020_autumn_q2_04 (75°+125°−180° = α = 20°), 2025_spring_q1_04 |
| Plug in numbers, check the 4 answers differ (tie check) | solve-geo30-g006, card tip, geo30-advanced-p10 solution | METHOD | KEEP | 2023_winter_q2_03 (answers in α), 2023_autumn_q1_10 (statements in α, β, γ) |
| Units-digit tip (83°+54°+x = 180°) | card mem-lines-angles tip | METHOD | REMOVE | 0 real questions where the units digit decides the answer |
| Guided Q2: ⊥ to the same line → hidden parallel, x = 130° | q-r26-t30-01 + video solve-q-r26-t30-01 | CONTENT (type) | KEEP | Deciding parallelism before angle-chasing: 2024_winter_q2_14, 2021_spring_q2_20 |
| Guided Q3: segments on a line (AC, BD, AD → BC) | q-r26-t30-02 + video solve-q-r26-t30-02 | CONTENT (type) | UNSURE | Overlap-type segments: 0 real; type already in original (adv-p09, -p16) |
| Guided Q7: two bends (zig-zag) | q-r26-t30-03 + video solve-q-r26-t30-03 | CONTENT (type) | KEEP | 2020_spring_q2_15 (multiple bends), 2023_winter_q2_03 |
| Practice -04: "looks parallel" → cannot be determined | q-r26-t30-04 (foundation) | CONTENT (type) | KEEP | 2024_winter_q2_14 (parallelism must come from the angles, not the look) |
| Practice -05: U shape with 4x+10, 2x+20 | q-r26-t30-05 (foundation) | CONTENT (type) | KEEP | 2019_winter_q2_04 (U), 2019_spring_q1_09 (algebraic angles 2y−30°, x+y between parallels) |
| Practice -06: ten equally spaced points, count the gaps | q-r26-t30-06 (advanced) | CONTENT (type) | KEEP | 2025_spring_q1_02 (1 real: equally spaced points A–D, find B) |
| Practice -07: two bends | q-r26-t30-07 (advanced) | CONTENT (type) | KEEP | 2020_spring_q2_15 |
| Practice -08: C shape with letters (360° − α − β) | q-r26-t30-08 (advanced) | CONTENT (type) | REMOVE | 0 real (C shape) |
| Practice -09: 107°+73° inside a U → lines parallel | q-r26-t30-09 (advanced) | CONTENT (type) | KEEP | 2021_spring_q2_20, 2024_winter_q2_14 |
| foundation p14 rewritten as a C-shape question and moved to advanced | geo30-foundation-p14 | CONTENT (type) | REMOVE the rewrite (restore original p14 in foundation) | 0 real (C shape) |

Counts: KEEP 20 (of which 6 FIX), REMOVE 4, UNSURE 1.

## TO REMOVE
- Video solve-geo30-g007 (Q6, old Q4): slide "The C shape" (inserted after "The zig-zag rule"). Keep "The zig-zag rule".
- Card mem-lines-angles: row "Bent line (C shape)" (`α+β+x=360°`).
- Card mem-lines-angles: the units-digit tip (example 83° + 54° + x = 180°).
- Question q-r26-t30-08 (advanced practice, C shape with letters).
- geo30-foundation-p14: undo the C-shape rewrite and the move to advanced (restore the original stem/choices/figure/solution in foundation practice).

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- geo30-foundation-p09 (unplaced): "In the accompanying figure, a∥b. What is the value of α+β?"
- geo30-foundation-p15 (unplaced): "Three distinct parallel lines are intersected by a fourth line ... How many distinct points of intersection are formed?"
- geo30-foundation-p14: original question (a copy of guided Q4, bent line, a∥b, "What is the value of x?") replaced by a C-shape question and moved to geo30-advanced-practice.
- geo-001 slide "Right angle": the original sentence "on the exam there is almost always a dot in the square" was deleted. It is TRUE on the real exam (every right angle in the real figures is a square with a dot, e.g. 2020_autumn_q2_20, 2024_autumn_q2_02, 2026_spring_q1_16). Restore it.
- geo-001 vertical-angles slide: the 220° arc was removed from the figure (the teacher still writes 140°) – figure change only.
- solve-geo30-g007: the spoken line "That's it for lines and angles." was deleted (because new slides follow).
- geo30-advanced-p05: stem rewritten ("One of the angles measures 116°. Its adjacent supplementary angle and the angle x together form an angle of 136°" → "three lines meet at O … what is x?" with the numbers moved into a new figure).
