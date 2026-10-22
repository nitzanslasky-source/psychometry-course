# Topic 30 (Lines and Angles): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/03-Geometry-Original-Subtitles.txt`, lines 14-402 (all of it read): theory 14-146, advanced 148-402.
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t30.py`): geo-001 (4 parts),
  solve-geo30-g002, geo-004, solve-geo30-g005/-g006/-g007, solve-q-r26-t30-01/-02/-03, r26-t30-summary, r26-t30-summary-2;
  the base translation `studio-build/base-v18.html`; the practice list `scratchpad/ext/course/q30.txt`.
- Recording status (`python3 video_status.py`): **nothing in topic 30 is in `--list record`.** geo-001 (part 1) is in `reread`;
  geo-001-2/-3/-4 are in `send`; geo-004, every solve-geo30 video and every solve-q-r26-t30 video are `done`. So any restore
  below means re-recording a finished video.

**Match scale** (as in the t23 report). New numbers alone are not a change. SAME = same idea and every one of her methods.
CHANGED = same idea, but the method, example type or order differs. PARTIAL = part of her content or one of her methods is
missing. MISSING = no English equivalent.

**Her names.** "Z" stays "the Z" (geo-001-4). Her "small angles / large angles" (קטנות / גדולות) stays "small / large angles",
and like her, English skips the school names (alternate, corresponding...). הצבת מספרים → "plugging in numbers"; הברקה →
"an insight"; ספרת אחדות → "the last digits"; בניית עזר → "an auxiliary line"; עוגן → "an anchor".

**Id gaps (geo-001, g002, geo-004, g005-g007, then geo-009 = topic 31).** Her section is: theory video → one question → 10
self-practice → advanced intro → three questions → "let's go to the summary" → 10 self-practice. Item 003 is most likely her
first self-practice set and item 008 her summary or second practice set. Neither was a video with subtitles, and base-v18 has no
geo-003 / geo-008 id at all. Her summary video is not in the subtitle file, so it cannot be compared. English has two new
summaries instead (r26-t30-summary, r26-t30-summary-2).

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | פתיחה · Geometry on the exam | 17-21 | 5 of 20 questions are geometry, a quarter; mostly the rules; clever-idea questions are rarer | geo-001 slide 0 | SAME |
| 1b | ישר, קטע · Line, segment | 22-32 | Line through two points; axiom: exactly one straight line through two points; a line is infinite; a segment is bounded by two points | geo-001 slide 1 | SAME (English adds slide 2: count the gaps, not the points) |
| 1c | ישרים נחתכים, 360 · Intersecting lines | 33-36 | Two lines cross at one point, 4 angles, a full circle is 360 | geo-001 slide 3 | SAME (English adds the angle and vertex definitions and a 3-line, 6-angle example) |
| 1d | זווית ישרה · Right angle | 37-41 | 90°, perpendicular lines, the square with a dot (almost always on the exam); 90 = a quarter of 360 | geo-001-2 slide 1 | SAME (English adds "don't trust how it looks: only if it's marked, given or calculated") |
| 1e | חדה, קהה · Acute, obtuse | 42-47 | <90, >90; if one angle at a crossing is acute, the one next to it is obtuse, and the other way round | geo-001-2 slides 2-3 | SAME (the acute/obtuse-neighbour point appears in slide 3, adjacent angles) |
| 1f | זווית שטוחה · Straight angle | 48-53 | 180 = a straight line with a vertex, half of 360, 180 on each side | geo-001-2 slide 2 | SAME |
| 1g | זוויות צמודות · Adjacent angles | 54-63 | Two neighbouring angles from two crossing lines add up to 180; one acute, one obtuse; special case 90 + 90 | geo-001-2 slide 3 | SAME (English adds the warning that side-by-side angles NOT on one line need not add up to 180) |
| 1h | זוויות קודקודיות · Vertical angles | 64-73 | Vertical angles are equal; proof with 30 → 150 → 30, both completing to 180 on the two lines | geo-001-2 slide 4 (35 → 145 → 35) | SAME |
| 1i | חוצה זווית · Angle bisector | 74-75 | A line from the vertex that splits the angle into two equal angles, alpha and alpha | geo-001-3 slide 1 | SAME (English adds three numeric examples) |
| 1j | סימון זוויות · Naming angles | 76-87 | Greek letters alpha, beta, gamma, delta (delta looks like a lamed, so students call it "lamda", it doesn't matter); the three-letter name BAC, vertex in the middle; or the size in degrees | geo-001-3 slide 2 | SAME (her lamed/lambda remark is Hebrew-specific; English says "students sometimes mix up the names") |
| 1k | ישרים מקבילים · Parallel lines | 88-93 | Constant distance, distance is always perpendicular, they never meet | geo-001-3 slide 3 | SAME (English adds the arrow marks) |
| 1l | מקבילים וחותך · Parallels and a transversal | 94-114 | 8 angles; even = small, odd = large; all small equal (vertical + across the lines), all large equal; small + large = 180 (adjacent); the green/orange circle "cut out and moved down" | geo-001-3 slides 4-5 | SAME |
| 1m | ה-Z · The Z | 115-125 | Always look for the Z with parallels; the two angles in its corners are equal; school names not needed; from there to every other angle, equal or completing to 180 | geo-001-4 slide 1 | SAME (English adds why it works, and the turned Z). English adds slides 2-3: the U (180) and the three rules for proving lines parallel + "not drawn to scale" |
| 2 | שאלה: 75°, זווית ישרה · Q: parallels, 75° and a right angle (easy) | 129-144 | Small angles equal → 75 at line b; the angle x next to it: 75 + x = 90 → x = 15; **x is vertical to the "?"**, so ? = 15 | solve-geo30-g002 (64°, x = 26) | CHANGED: the English figure puts x directly next to the 64 inside the right angle, so **her vertical-angle step is gone** (it was already gone in base-v18). English adds the trap: 64 is the angle next to x |
| 3 | 10 שאלות תרגול עצמי · 10 self-practice (no video) | 146 | — | geo30-foundation-p01 … p10, plus p13, p17 and q-r26-t30-04 | SAME (all 10 kept with new numbers; base had 17 in this set, the current course has 13) |
| 4 | לימוד מתקדם – פתיח · Advanced intro | 149-156 | We'll practise few questions: a narrow topic; standalone questions exist, but mostly these rules are part of other geometry questions | geo-004 | SAME (English adds the "three things make it harder" list: crowded figure, letters, a missing line) |
| 5 | שני זוגות מקבילים · Q: two pairs of parallels, 86° and 53° (easy) | 158-209 | Could be solved with a parallelogram or triangles, but lines only; (1) one pair at a time, ignore the rest of the figure: 86 moves to b, 53 moves to c; 53 + 86 + ? = 180, add tens then ones (139) → 41. (2) Units-digit shortcut: 3 + 6 = 9, so ? ends in 1, eliminate 9, 7, 3; "save every second" | solve-geo30-g005 (77° and 56°, x = 47) | SAME (both methods, the "ignore the rest" habit, tens-then-ones, and "every second matters". With the new numbers the digits carry, 7 + 6 = 13, and English explains the 3 + 7 that makes a ten; it still works). English adds the Z as the way to see the move |
| 6 | ארבעה ישרים בנקודה · Q: four lines at a point, delta = ? (hard) | 212-348 | Letters instead of numbers = the main way geometry gets harder; 3 ways. (1) Math: the anchor (360 or 180); neighbours 180 − alpha, beta, gamma; four angles make a straight line; brackets (a plus doesn't affect them, a minus would); move terms → delta = alpha + beta + gamma − 360; "how do you spot it on the last question?" (2) Plug in: **it looks obtuse, so plug in an obtuse, round angle (150; 140 or 160 also fine)**; the same number for all three, so the choices are easy to check; "numbers roll easily, letters don't"; delta = 90; eliminate 3 choices (the drawback of plugging in); 450 − 180: "some see it's too big", or 450 − 200 + 20 = 270. (3) Insight: alpha + beta + gamma = 360 + delta (delta counted twice). **Verdict:** the insight is shortest but most students don't see it under pressure; strong students can do the math; for most students plugging in is much simpler and the answer is certain | solve-geo30-g006 (m, n, k; 140 → x = 60) | PARTIAL: all three methods and the brackets warning are there; English adds the balance rule for moving terms, why plugging in is allowed, the "x > 0" check and the "if two choices tie, plug in again" check, and links the insight to the overlap rule (q-r26-t30-02). **Missing:** (a) her closing verdict (most students: plug in, it turns a very hard question into an easy one; the math way is fine if you are strong). Base-v18 had it, the current script cut it (R35 "no verdict"). (b) "It looks obtuse, so plug in an obtuse round angle": English says only "easy numbers that the figure allows" (the obtuse tip survives only in r26-t30-summary-2). (c) "Numbers roll easily". (d) The 450 − 200 + 20 mental step (English keeps only "far more than sixty, out") |
| 7 | קו שבור בין מקבילים · Q: bent line between parallels, 45° and 50° (hard) | 351-398 | Hard because of the broken line; what an auxiliary line is; other options (extend a piece → exterior angle of a triangle; a perpendicular → two triangles), "fine if you did"; lines only: a line through the bend parallel to a and b; small angles equal → 45 + 50 = 95; "once you add it the question is simple; the difficulty is thinking: which line, and that you need one at all" | solve-geo30-g007 (36° and 62°, x = 98) | SAME (every point kept, the Z named for each part). English adds the zig-zag rule (left-pointing = right-pointing angles) as a second method |
| 8 | סיכום · "Let's go to the summary" | 399-400 | (her summary video is not in the subtitle file) | r26-t30-summary, r26-t30-summary-2 | cannot compare (not counted) |
| 9 | 10 שאלות תרגול עצמי · 10 advanced self-practice (no video) | 402 | — | geo30-advanced-p01 … p11, p16, q-r26-t30-07 | SAME (all 10 kept with new numbers; base had 17, the current course has 13) |

**Count by row (19 counted rows):** SAME 17 · CHANGED 1 (2) · PARTIAL 1 (6) · MISSING 0.

### Count by video (her units)

| Unit | Match |
|---|---|
| Theory lesson (1a-1m) | SAME (nothing of hers missing; English adds gaps, U, parallel-proof rules, "not to scale") |
| Q 75° / right angle | CHANGED (vertical-angle step gone with the new figure) |
| 10 foundation practice | SAME |
| Advanced intro | SAME |
| Q two pairs of parallels | SAME |
| Q four lines at a point | PARTIAL (verdict, "plug in an obtuse round angle", 450 − 200 + 20) |
| Q bent line | SAME |
| 10 advanced practice | SAME |

**By video: SAME 6 · CHANGED 1 · PARTIAL 1 · MISSING 0** (8 units including the two practice sets; her summary not compared).

---

## 2. English with no Hebrew equivalent

- geo-001 slide 2: points on a line, count the gaps (5 points = 4 gaps). This sets up q-r26-t30-02.
- geo-001-2 slide 1: "don't trust how an angle looks" (90 only if marked, given or calculated); slide 3: the warning about side-by-side angles not on one line.
- geo-001-4 slides 2-3: the U (sum 180), the three rules that prove two lines parallel, "figures are not drawn to scale".
- geo-004: the "three things make it harder" list.
- solve-q-r26-t30-01: proving a ∥ b (both perpendicular to c), then the usual move.
- solve-q-r26-t30-02: segments on a line, AB by subtraction, plus the overlap rule (used again in g006 and later topics).
- solve-q-r26-t30-03: a line bent twice, the zig-zag rule and a parallel line through each bend.
- The zig-zag rule as a second method in g007.
- r26-t30-summary and r26-t30-summary-2 (her summary exists but has no subtitles).

## 3. Recommendations

| Missing from English | Where it would go | Length | Recorded? | Recommendation |
|---|---|---|---|---|
| Her verdict in the four-lines question: the insight is shortest but rarely seen in time; strong students can do the math; for most, plugging in is much simpler and the answer is certain | solve-geo30-g006, end of slide 4 | 3-4 sentences | yes (done) | OPTIONAL: it is real strategy advice from her, cut on purpose by the R35 "no verdict" rule. Her call whether that rule should give way here |
| "It looks obtuse, so plug in an obtuse, round angle" | solve-geo30-g006 slide 2, in place of "easy numbers that the figure allows" | 1 sentence | yes (done) | OPTIONAL: it is how she picks the numbers. It is already in r26-t30-summary-2 ("Looks obtuse? Plug in a hundred thirty"), so the student does get it once |
| 450 − 200 + 20 mental subtraction | solve-geo30-g006 slide 3 | 1 sentence | yes (done) | NOT NEEDED: with English's 420 − 180 the "far more than sixty, out" reasoning is her own first route |
| Vertical-angle step in the first question | solve-geo30-g002 | — | yes (done) | NOT NEEDED: the English figure has no vertical step, and vertical angles are fully taught in geo-001-2 slide 4 |
| "Numbers roll easily, letters don't" | solve-geo30-g006 slide 2 | 1 sentence | yes (done) | NOT NEEDED: English says "With numbers the neighbors are easy" |

**RESTORE list: none.** Nothing of hers is wrong in English. The only real loss is the g006 verdict (OPTIONAL). Every topic-30
video is already recorded, so any change means re-recording.
