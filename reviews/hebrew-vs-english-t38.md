# Topic 38 (Geometric reasoning): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/03-Geometry-Original-Subtitles.txt`, lines 9461-10234 (all of it read).
- English: `scratchpad/ext/course/t38.txt` (every video's spoken text) and `q38.txt` (practice questions), the current flow in
  `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`, the base translation `studio-build/base-v18.html` (flow checked).
- **Recording status:** topic 38 has no reading scripts in `ai_scripts/` yet (only `r26-t38-summary.json`), so none of its
  videos are in the `video_status.py` tracker. **Nothing in topic 38 is recorded**; every target below is unrecorded.

**Match scale.** New numbers alone are not a change (memory rule *questions-differ-from-hebrew*).
SAME = same idea and every one of her methods. CHANGED = same idea, but the method, the example type or the order differs.
PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Her names carry over:** יעילות צורה → "shape efficiency" (the country rule kept); מפתח זווית → "angle opening" / "the rods rule";
מינימום-מקסימום עם עוגן → "min–max with an anchor"; שרטוטים גמישים → "flexible drawings / diagrams that can change"; הקצנת שרטוט →
"exaggerate the drawing"; תיקון השרטוט → "make the drawing match the givens"; מעבר חצייה → "the crosswalk"; בניין קומות → "the building";
זאב בעור של כבש → "a wolf in sheep's clothing". Her pun "האלכסון הוא אסון" has no English version (untranslatable, nothing lost).

**Id numbering.** geo-172 (lesson 1, efficiency) + g173, g174; geo-175 (lesson 2, min–max) + g176; geo-177 (intro to the question
lesson); g178-g187 (her 10 sample questions). 16 of her segments, 16 ids, in her order; no gaps.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1 | יעילות צורה · Shape efficiency | 9463-9506, 9533-9560 | Geometric understanding = solve with no calculation; for those who find it harder. Circle = most efficient (largest area : perimeter); a closed string → circle has the most area; **the country rule** (most land, least border); closer to a circle → more efficient. Demo: a very thin rectangle (lots of border, no area), widen it → area ×2, ×3 for a little border. "5 seconds on the exam." Next: flexible drawings, min–max | geo-172 (all slides incl. "Long and thin") | SAME (in English the thin-rectangle demo comes before the two questions, in hers after them; nothing lost) |
| 2 | אותו היקף – שטח מקסימלי · Equal perimeters, greatest area | 9508-9518 | Triangle, square, pentagon, hexagon → the hexagon hugs a circle most → greatest area | solve-geo38-g173 (… octagon, perimeter 30) | SAME (English adds "the sides are shorter but the boundary is the same") |
| 3 | מחומש משוכלל מול לא משוכלל · Regular vs non-regular pentagon, equal areas | 9520-9532 | Area + perimeter → efficiency; the regular one is more circle-like → less perimeter → the non-regular one has more border | solve-geo38-g174 (octagonal flower beds, 60 m²) | SAME (English adds a rectangle check, 10×10 vs a stretched rectangle, and "same number of sides") |
| 4 | מינימום-מקסימום · Min–max: angle opening | 9562-9652 | Move the vertex away from the segment → the angle closes (toward 0), closer → opens toward 180; fixed vertex, longer segment → bigger angle (α inside β); angles on an arc: farther → smaller; angle on a diameter: on the circle 90, inside > 90, outside < 90; min–max "with an anchor" (a familiar base situation, then a change). Her closing words "we've finished geometry, I wish you…" come here | geo-175 (all slides) | SAME (English adds: "straight away" matters; the farthest-apart slide (diagonal, diameter, cylinder 9 & 4 → √145); inscribed angles on the same arc are equal). Her "finished geometry" farewell is moved to the real end of the topic (g187) |
| 5 | משולש 6, 8, 11 · Triangle 6, 8, 11, compare α with 90 (anchor) | 9626-9652 | Strong students see 6-8-10; otherwise the choices compare α with 90 → anchor 90 → if α were 90 the side would be 10; it is 11 → the angle opened → α > 90 | solve-geo38-g176 (8, 15, 18; anchor 8-15-17) | SAME (English adds the squares check 324 > 289 and "the longest side only says α is the largest angle") |
| 6 | הבנה גאומטרית – פתיח · Intro to the question lesson | 9661-9665 | Last lesson we met the topic; now high-level questions and more nuances | geo-177 | SAME (English adds "the drawing suggests, it doesn't prove; read must / could / cannot") |
| 7 | טרפז, DE ⟂ BC · Triangle vs trapezoid, can't know (hard) | 9667-9712 | Looks simple, but: hard, end of the section, a "none must be true" choice → suspect it. Flexible drawing: legs only look equal (if isosceles the trapezoid wins); stretch BC keeping every given → the triangle wins; it depends on EC vs the sum of the bases → can't know. "A wolf in sheep's clothing" | solve-geo38-g178 (KLMN, NF ⟂ LM) | SAME (every step). English adds a numeric check (FM 3 / 7 / 12 → smaller / equal / bigger), "what is free? push it to the end or the middle", and the caution that "cannot be determined" is rare, so test it with two figures |
| 8 | קוטר ומיתר מאונך – צביה, שלומי, ארז · Diameter and a perpendicular chord, three claims (hard) | 9714-9761 | CD is only "a chord", not a diameter → flexible → move CD; a diameter is a symmetry line → Tzvia right; Shlomi not necessarily; Erez right (halves) → only Shlomi wrong. "Looks simple but at the end of the section, be careful" | solve-geo38-g179 (Lily / Ethan / Grace) | SAME |
| 9 | מקבילית – טווח אלפא · Parallelogram, exact range of α (medium) | 9763-9808 | Every choice gives a min and max → min–max → check the edges: adjacent angles sum to 180; β → 90 (plug in 90, not 89.99…) → α > 30; β → 0 → α < 120; also by exaggerating (a rectangle). **Her time-saver: after crossing out 1 and 3, choice 4 has 150, and 150 + 60 is already more than 180 → impossible → mark 2** | solve-geo38-g180 (∠BAC = 50, β < 70 → 60 < α < 130) | CHANGED: checking the edges and exaggerating are kept; **her time-saver is replaced by a different one**: "2 and 4 differ only in ≤ vs <, and the edges come from values β never reaches, so mark 4". Her "an end value that breaks the 180 sum" idea does not appear (the English choices don't offer it) |
| 10 | ישרים מקבילים, α < β < γ < 90 · Slanted segments between parallels (medium+) | 9810-9866 | **Fix the drawing first**: in the given figure all angles look equal (~90), so redraw: α sharpest → longest segment, β a bit less, γ as is; then "you just see it by eye". The crosswalk: the more slanted, the longer. BD vs CD: undetermined (not fixed) → possible → out; EF vs CD, AB vs CD; three out → mark the fourth, check it in the lesson. "Fixing the drawing made it much simpler" | solve-geo38-g181 (c ∥ d; KL, MN, PQ) | CHANGED: the crosswalk rule, the undetermined claim and the exam routine are kept, and English adds why (same height, longer hypotenuse). But **the English figure already matches the givens** ("Here the drawing already agrees"), so her key move, actually redrawing a misleading figure, is only described as a hypothetical. The closing line "fixing the drawing made it a lot simpler" then refers to a step that never happened |
| 11 | כדור – שני חיתוכים · Sphere, which cut gives more surface (medium+) | 9869-9902 | Both pieces' surface = the sphere + the two cut faces; the sphere is the same → compare the cut faces; chord principle: the diameter is longest, farther from the centre → shorter (toward 0); distances 1 and 2 → cut A | solve-geo38-g182 (radius 6; distances 3 and 1) | SAME (English adds an exact check, 36 − 9 vs 36 − 1) |
| 12 | שתי מקביליות, 60° ו-50° · Two parallelograms, same sides (hard) | 9905-9980 | (1) AC > AB: triangle inequality (1 < AC < 3); **or an anchor: a 60° angle → build an equilateral triangle 1, 1, 1 on it → AC reaches farther → > 1.** (2) AC > EG: same sides, bigger angle → bigger opening. (3) Equal areas: same base, heights by the angle → definitely false = the answer; also by exaggerating (80° vs 30°); max = rectangle (2), min → 0. Exam: cross out 1, 2, glance at 4 (equal perimeters, obviously true) → mark 3 without proving it | solve-geo38-g183 (4 and 8; 70° vs 30°) | CHANGED: everything is kept except **the anchor: her equilateral-triangle anchor is replaced by a 30-60-90 one** ("careful, 4 and 8 with 60° are NOT equilateral … AC is 4√3"). With sides 4 and 8 her 1-1-1 picture doesn't fit directly, and the English anchor is correct. English adds "past 90° the height shrinks again (110° = 70°)" |
| 13 | חוצה זווית במשולש ישר זווית · Angle bisector in a right triangle (hard) | 9983-10096 | Four claims, each several ways. (1) α vs β: higher vertex on the same segment → sharper (like central vs inscribed angle); exaggerate; the building (floors D, A); exterior angle β = α + x. (2) AC vs DC: the perpendicular is the shortest (crosswalk), farther → longer; exaggerate; the building; Pythagoras with a shared leg. (3) α vs x: undetermined → plug in numbers (80 → x = 5; 10 → x = 40); exaggerate; three out → mark. (4) AD vs BD: "equal angles, equal segments" is a trap; farther from the vertex → bigger opening; proof: a perpendicular from D → congruent triangles → DB = a leg < AD | solve-geo38-g184 (RST, TP bisects ∠T) | SAME (every argument; numbers 70 → 10 and 20 → 35) |
| 14 | ריבוע ומשושה משוכלל · Square vs regular hexagon, which is false (hard) | 10099-10143 | Same perimeter → hexagon more area; same area → square more perimeter; both inscribed in a circle → more sides, closer to the circle ("a circle is a polygon with infinitely many sides"; the grey pieces picture) → hexagon more area; on the exam mark 4; in the lesson: inscribed perimeters also grow with the sides (octagon, decagon). "Easy if you master efficiency, though it's second-to-last" | solve-geo38-g185 (equilateral triangle vs hexagon) | SAME (English adds a triangle-inequality reason for the perimeters) |
| 15 | ניסור קובייה – מספר פאות · Cut a cube in two, impossible number of faces (hard) | 10145-10184 | Trial and error: halves → 12; **min–max insight: the answers have a max and a min, the problem is usually at the extremes; reached the max (12) → mark the min (9)** ("few think of it; not always, usually"); continue: diagonal → 2 prisms → 10; cut a corner → 4 + 7 = 11 → mark 9 | solve-geo38-g186 (a block of cheese; impossible 16) | SAME (the same insight, mirrored: the English reaches the minimum, 10, and the impossible answer is the maximum, 16). English adds a proof (at most 12 + 2 = 14) |
| 16 | n מעגלים במלבן – נקודות השקה · n circles in a rectangle, tangency points (medium+) | 10187-10230 | (1) Understanding: each side's count (n, n, 1, 1) → 2n + 2. (2) Plug in: **not 1 or 2, they usually fit two answers; plug in 3**; count 8; eliminate every non-8; don't mark until three are out | solve-geo38-g187 (three rows → 2n + 6) | SAME (both ways; English shows the n = 2 clash on purpose). Her end-of-geometry farewell is placed here |
| 17 | 20 שאלות תרגול עצמי · 20 self-practice questions | 10234 | — | geo38-core-p01 … p27 (q38.txt) | SAME (kept, more added) |

**Count by row (17 rows):** SAME 14 · CHANGED 3 (9, 10, 12) · PARTIAL 0 · MISSING 0.

### Count by video (her 17 units)

| Unit | Match |
|---|---|
| Lesson 1 efficiency | SAME |
| Q equal perimeters (g173) | SAME |
| Q equal areas (g174) | SAME |
| Lesson 2 min–max | SAME (farewell moved to g187) |
| Q anchor 90 (g176) | SAME |
| Intro to the question lesson (geo-177) | SAME |
| Q trapezoid flexible (g178) | SAME |
| Q diameter and chord (g179) | SAME |
| Q parallelogram range (g180) | CHANGED (her 150 + 60 > 180 time-saver replaced) |
| Q slanted segments (g181) | CHANGED (the figure needs no fixing, so her "fix the drawing" move isn't shown) |
| Q sphere cuts (g182) | SAME |
| Q two parallelograms (g183) | CHANGED (equilateral anchor → 30-60-90 anchor) |
| Q angle bisector (g184) | SAME |
| Q polygons efficiency (g185) | SAME |
| Q cutting a solid (g186) | SAME |
| Q tangency points (g187) | SAME |
| 20 practice questions | SAME |

**By video: SAME 14 · CHANGED 3 · PARTIAL 0 · MISSING 0.**

---

## 2. English → Hebrew (English topic-38 parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| geo-175 slide "Farthest apart" + "straight away" and same-arc warnings | Greatest distance (diagonal, diameter, cylinder); moving along the circle keeps the angle | none | no |
| solve-geo38-g173 slide 2, g174 slide 2 | "The boundary, not the side"; the rectangle check | none | no |
| solve-geo38-g176 slide 3 | The squares check (c² vs a² + b²) | none | no |
| geo-177 slide 2 | "The drawing suggests, it doesn't prove; must / could / cannot" | none | no |
| solve-q-r26-t38-01 | Two sides 6 and 10, free angle → greatest area at 90° (30); trap 24 | none (her rods / opening rule is the seed) | no |
| solve-q-r26-t38-02 | Trapezoid diagonals: same base, apex on a parallel → equal areas; ABE = DCE | none | no |
| solve-geo38-g178 slide 4 | Numeric demo; "cannot be determined is rare, test it" | none | no |
| solve-geo38-g183 (part) | Past 90° the height shrinks again | none | no |
| solve-geo38-g186 slide 4 | Proof that 16 is impossible | none | no |
| r26-t38-summary, mem-geo-reasoning | Summary and reference card | none | no / — |
| practice geo38-core-p21 … p27 and the r26 practice | Extra practice | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **g181: actually fixing a misleading drawing** (her figure showed all angles ≈ 90°, and the lesson was to redraw it to match α < β < γ) | the g181 question figure: draw the three segments at about the same angle, then slide 1 redraws them ("make α the sharpest, β a bit less, leave γ"), 2-3 sentences; or, if the figure stays, change the closing line | no | **Restore.** It is the named skill of this question ("fixing the drawing"), it is cheap (a figure change plus 2-3 sentences), and the current closing line "fixing the drawing made it a lot simpler" describes a step the English never does |
| 2 | g180: her time-saver "an end value that breaks the sum (150 + 60 > 180) is impossible" | solve-geo38-g180 slide "Save time": give choice 2 an impossible end (e.g. "60 < α < 150", since 150 + 50 > 180) instead of the ≤ / < twin, then use her shortcut | no | **Optional.** The English shortcut (edges are excluded) is also good; hers teaches checking the answers against the angle sum, which is more general. Either one, or both (1 sentence each) |
| 3 | g183: the equilateral-triangle anchor for AC > AB | — | no | **Not needed.** With sides 4 and 8 it doesn't fit, and the English 30-60-90 anchor is correct; the triangle inequality already proves the claim |

## 4. Wrong in the English

- solve-geo38-g181: the last line, "fixing the drawing made it a lot simpler", contradicts slide 1 ("Here the drawing already
  agrees"). See 3.1.
- Nothing else is wrong compared with her.
