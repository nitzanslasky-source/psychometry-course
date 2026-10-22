# Hebrew restore: topic 33 (geo-079, g090, g092), topic 51 (pt-q16), topic 52 (ch52-change), summary pages 31 / 32

2026-10-22. Source: reviews/hebrew-vs-english-t33.md (rows 6, 17, 19 and items 1, 3, 4), -t51.md (row 4b, item 1),
-t52.md (row 11d), -t32.md (row 71), -t31.md (row 34). Hebrew checked in ~/Downloads/03-Geometry-Original-Subtitles.txt
(3670-3685, 4131-4166, 4210-4255) and modulesV51.py / modulesV52a.py (the base translation of her lines).
Brief: scratchpad/BRIEF-extfix.md (conditions 1-6), guide rules W17-W23 and R37.

Files changed:
- `studio-build/math_patches/_ai_vis_t33.py` (geo-079 slide 4 "π is a number"; solve-geo33-g090 and -g092 rewritten
  with new numbers, their figures and board rows)
- `studio-build/math_patches/t33.py` (question data: geo33-g090 and geo33-g092 stem, choices, explanation, question
  figures; the base-video rewrite pairs)
- `studio-build/math_patches/_ai_vis_t51.py` (solve-pt-q16 slide 0 and slide 2, method 2)
- `studio-build/math_patches/_ai_vis_t52.py` (ch52-change slide 5 "Week by week")
- `studio-build/summary_pages/t32.json` (one table row)
- The ai_scripts JSONs of the five videos were rewritten by the spec runs.
Before-copies: scratchpad/hr-geo/before/ (all the files above, as they were this morning).

**Recording status (condition 1):** `video_status.py --list record` lists geo-079, solve-geo33-g090, solve-geo33-g092,
solve-pt-q16 and ch52-change, and none of them has a folder in ~/Documents/Course.recordings/_reading/. So all five
were edited directly; nothing recorded was touched. Numbering below = slide.paragraph as in the brief and the prompter
dump (both 0-based: geo-079 slide 4 = "π is a number").

## 1. geo-079 slide 4 "π is a number": π = 3.14159…

Her line (geo 3676-3678): "π is about 3.14 … because it goes on, 3.141592 and so on … 3.14 is enough, even 3.1 for the
exam; all we need to know is that it's a bit more than 3." g089 later uses 3.14 < π < 3.15, never taught before.

- **4.1 BEFORE:** "It just isn't a round number. Its digits after the decimal point never end, so instead of writing
  them, we give it a special sign, the letter pi. That's easier to write and easier to see in the formula."
- **4.1 AFTER:** "It just isn't a round number. Pi is three point one four one five nine, and so on. Its digits after
  the decimal point never end, so instead of writing them, we give it a special sign, the letter pi. That's easier to
  write and easier to see in the formula."
- **4.2 BEFORE:** "… that's all we need to know about pi. It's a bit more than three."
- **4.2 AFTER:** "… that's all we need to know about pi. It's a bit more than three. We need its first digits, three
  point one four, only when the choices are close ranges of numbers."
- **Board:** new typed row `π = 3.14159…` (f3b7b) under "π is a fixed number…", written at "Pi is three point one four
  one five nine"; pointed at again at "We need its first digits". 3.14159… shows both of g089's bounds (more than 3.14,
  less than 3.15) without teaching them here.
- **Condition / rules:** the spec check flags "about + decimal" as a decimal estimate (memory: no decimal estimates),
  so π is given as its exact digits, not "about 3.14"; "a bit more than three" stays the tool for rough checks.
  g089 itself is NOT changed (teacher decides; t33_CHANGES.md "LEFT").
- **Read-aloud:** ready. "its first digits" names what is needed; no loose "it".

## 2. solve-geo33-g090 and solve-geo33-g092: numbers changed so her "spot the triple" step works (W23)

**g090** (Hebrew 5-12-13 → 13π; English was 12-35-37 → 37π): now **9, 12, 15 → 15π**. 9-12-15 is 3-4-5 × 3, the
multiples taught in geo-024 ("multiply three, four and five by the same number"). 7-24-25 was not used: the course
tells students NOT to learn triples beyond 3-4-5 and 5-12-13, so they would not recognise it.
- Question data (t33.py `_rn_q`): stem "9 cm, 12 cm and 15 cm"; choices 30π / **15π** / 7.5π / 81π (answer still 2,
  same trap pattern: d used as r, no 2, short leg squared); explanation (triple, check 81 + 144 = 225, d = 15, C = 15π);
  question figure redrawn 9 : 12 : 15. Base-video rewrite pairs updated.
- Script: slide 0 numbers only. Slide 1 (was: squaring 35 and 37 with long splits) is now:
  "Do these three numbers look familiar? They all divide by three. Nine is three times three. Twelve is three times
  four. And fifteen is three times five." / "So the sides are the Pythagorean triple three, four, five, times three. We
  learned that a triple times any number is still a right triangle. So we see the right angle without calculating any
  squares." / "If you don't spot the triple, check Pythagoras. Nine squared plus twelve squared is eighty-one plus a
  hundred forty-four, which is two hundred twenty-five. And fifteen squared is two hundred twenty-five too." / (right
  angle at A, unchanged wording with 15) / NEW her line (geo 4150): "This step is new. Until now, we got a right
  triangle and found a missing side. Here we get three sides, and we have to see the right angle ourselves. So when all
  three sides are given, but no right angle is marked, look for a triple." (replaces "This is the Pythagorean test we
  learned…" + "Use this test when…"). Inscribed-angle rule, BC = d = 15, C = π × 15 = 15π, choice 2: same text, new numbers.
- Slide 2 kept both of its methods: the difference of squares, now framed as the tool "for sides that aren't a triple
  you know" (15² − 12² = 3 × 27 = 81 = 9²; "With big sides, this way saves a lot of work."), and the traps 30π
  (choice 1) and 7.5π (choice 3) in their own paragraph.
- Board: rows 9 = 3×3, 12 = 3×4, 15 = 3×5, "the triple 3, 4, 5 times 3", 9² + 12² = 81 + 144 = 225, 15² = 225,
  BC = d = 15, C = 2πr = π×d, C = π×15 = 15π; slide 2 rows (15−12)(15+12), = 3×27 = 81 = 9², the two trap rows.
  The colour copy (triangle + dashed circumscribed circle, BC as diameter) redrawn: the circle really passes through
  all three vertices (radius 129.375 from the midpoint of BC, checked).

**g092** (Hebrew radii 1, 2, 3 → 3-4-5 → 1.5π; English was 6, 14, 15 → 20-21-29 → 9π): now **radii 3, 6, 9**.
Geometry checked: for 3-4-5 sides the radii must be k, 2k, 3k (r_A + r_B = 3k, r_A + r_C = 4k, r_B + r_C = 5k), so
any choice is a multiple of hers; k = 3 gives AB = 9, AC = 12, BC = 15, right angle at A (opposite BC), circumference of
A = 6π, highlighted arc = ¾ × 6π = **4.5π**. Distances in the drawn figure equal r + r exactly (108/144/180 px at 12 px/cm).
- Question data: stem "3 cm, 6 cm and 9 cm"; choices 6π / 4π / **4.5π** / 3π (answer 3; choice order kept: whole circle,
  ⅔, ¾, half); explanation; question figure; base-video slides rewritten.
- Script: every number recomputed (6π whole circle → choice 1 out; 3π half → needs 180° at A → choice 4 out; her 50%
  guess kept). Slide 1: "Nine, twelve, fifteen. We need the angle at A, so let's look at the three sides. Do they look
  familiar? They're three, four, five, times three. Again a Pythagorean triple, like in the circumscribed circle
  question." / "If you don't spot it, check Pythagoras. Eighty-one plus a hundred forty-four is two hundred twenty-five,
  and that's fifteen squared." (replaces 20² = 400, 21² = 441 split, 29 × 30 − 29 = 841). Slide 2: "Three quarters of
  six pi. Let's find a quarter first. Six pi divided by four is one and a half pi. So three quarters is three times one
  and a half pi, which is four and a half pi. Choice number three is our answer, and I'll see you in the next question."
- **Cut:** the difference-of-squares tail of g092 (29² − 21² = 8 × 50). It existed only to avoid 29²; with 15 and 12
  the squares are exam-level, and the same tool was just shown in g090 two questions earlier (W22: no repeat). Every one
  of her methods is in (both eliminations, the 50% guess, the triple, ¾ of the circumference).
- Board: rows AB = 3 + 6 = 9, AC = 3 + 9 = 12, BC = 6 + 9 = 15, "9, 12, 15: the triple 3, 4, 5 times 3",
  81 + 144 = 225 = 15², ∠A = 90° (one column, after the frames showed the second column running off the slide; the
  triangle-of-centres figure was enlarged). Slide 2 rows 6π ÷ 4 = 1.5π, 3 × 1.5π = 4.5π. The pen row "half the circle:
  ∠A = 180°" now ends ", no" instead of ✗.
- Duplicates: 9-12-15 is not her g090/g092 numbers (5-12-13; 1-2-3). It now appears in both g090 and g092 (as the brief
  asked); her g092 itself says "again a Pythagorean triple".
- **Read-aloud:** ready. "the circumscribed circle question" names g090; "it" in "If you don't spot it" = the triple
  just named.

## 3. solve-pt-q16: her "where is the π?" pattern (slide 0), triangle moved into method 2 (slide 2)

Her method (Q19, base modulesV51.py 1289-1294): the pattern of the calculation rules out choices before any number;
sector − triangle → "π minus a number"; "number − π" and "π / number" out; "sometimes only one choice has it right,
sometimes none". It replaces the decimal bound 3 < π < 3.2 (against the no-decimal-estimates rule), so that bound and
the 0.5-0.6 range are gone. Kept: her negative-area way (slide 1, unchanged, whole-number bound π < 4) and the partial
calculation (slide 2), now with the triangle as its check.

- **Slide 0 title:** "A justified size bound" → "Where is the π?"
- **0.2-0.5 BEFORE** (5 paragraphs): "Let's start with an estimate, after one small calculation…" / triangle legs by
  Pythagoras / area 1 and sector π/2 / "use these bounds for pi: more than three, and less than three point two… between
  zero point five and zero point six" / "(1) four minus pi … more than zero point eight… out" / "(3) … more than one point
  five… out".
- **0.2-0.7 AFTER:**
  - 0.2 "Let's start with estimation, before any numbers. First we look at the pattern of the calculation, and ask,
    where is the pi?"
  - 0.3 "The pi is in the sector. The sector is part of the circle, and the circle's area is pi r squared. The triangle
    has only straight sides, so its area has no pi. So sector minus triangle gives the pattern pi minus a number. The pi
    can come with a fraction, like pi over two. But it comes first, and a number is taken away from it."
  - 0.4 "Choice number one says four minus pi. That's a number minus pi, the opposite pattern. Here the pi is the part
    taken away, so choice number one is out."
  - 0.5 "Choice number three says pi over root two. That's pi divided by a number, and nothing is taken away. The
    triangle is missing, so choice number three is out too."
  - 0.6 "Choice number two says one half, times pi over two minus two. The half multiplies both parts, so it's pi over
    four, minus one. Choice number four says pi over two, minus one. Both have the pattern pi minus a number, so this
    test can't split them."
  - 0.7 "Sometimes the pattern rules out three choices, and sometimes none. Here it ruled out two, in seconds. And it
    works only because we know which part has the pi: here, the sector."
- **Slide 2 BEFORE (2.4-2.6):** "The shaded area is pi over two, minus the triangle's area. We found that the triangle's
  area is one. …" / "Choice number two has a half outside its whole bracket…" / "This is a partial calculation… A piece
  can rule choices out, but the answer still has to fit the whole shaded area."
- **Slide 2 AFTER (2.4-2.8):** "Now let's peek at the choices. Which of them has the sector, pi over two? Choice number
  four, pi over two minus one, has it. Choice number two has a half outside. The half multiplies the pi over two too, so
  it gives pi over four. That's not our sector, so choice number two is out." / "Choice number one has minus pi, and
  choice number three has pi over root two. Those two don't have pi over two at all. So the sector alone leaves only
  choice number four. To be sure, let's check the other piece, the triangle." / (the triangle paragraph moved from
  slide 0, unchanged) / "The triangle's area is leg times leg, divided by two. The legs are equal, so leg times leg is a
  leg squared, two. Two divided by two is one. So the shaded area is pi over two minus one. That's exactly choice number
  four, our answer." / "This is a partial calculation: find a useful piece, then look at the choices. Here the sector
  alone ruled out every choice but one. I'll see you in the next question."
- **Board slide 0** (right column, each at its clause): "Shaded = sector − triangle"; "Where is the π? In the sector";
  "Pattern: π (with a fraction) − a number"; "(1) 4 − π: a number − π, no"; "(3) π/√2: nothing taken away, no";
  "(2) π/4 − 1 (4) π/2 − 1". Crosses on choices 1 and 3 at "out". Slide 2: the circle/sector rows moved beside the
  pizza figure; the triangle rows (2 + 2 = 4, 2/2 = 1) and "Shaded = π/2 − 1" under it. Removed items: f4bound,
  f4range, f4reject1, f4reject3 (f4sector is still defined but no longer shown).
- **Condition stated:** the pattern works only when we know which part has the π (0.7); it can rule out none (0.7).
- **Maths:** π/2 − 1 ≈ 0.57 (choice 4); ½(π/2 − 2) = π/4 − 1 < 0; 4 − π and π/√2 are not of the form (π-part) − number.
- **Read-aloud:** ready. "it" in 0.7 = the pattern; "Those two" in 2.5 = choices 1 and 3, named in the sentence before.

## 4. ch52-change slide 5 "Week by week": the flat line that is a rise

Her recap (base modulesV52a.py 1599-1601): "here the line is straight, but in fact there's a rise; here it goes down,
and in fact there's no change."
- **New 5.7 (after "So at the end of week six there were seventy-five volunteers."):** "Now let's bring the line back,
  to see how it fooled us here. Into week four, the line is flat, so it looks like no change. But the point of week four
  is plus five, so five volunteers joined."
- **New 5.8:** "Into week five, the line goes down, so it looks like a drop. But the point is zero, so nothing changed.
  So a flat line can still be a rise, and a line going down can be no change."
- **Board / chart marks:** the chart (shown without the line for the calculation) turns back into the chart with the
  line at "bring the line back"; the flat piece from week 3 to week 4 is traced in amber at "Into week four, the line is
  flat"; the falling piece from week 4 to week 5 at "Into week five, the line goes down". Typed rows: "Into week 4 the
  line is flat, but +5: a rise" and "Into week 5 the line falls, but 0: no change" (same style as the slide-4 rows).
  Data checked: VOL weeks 3, 4, 5 = +5, +5, 0.
- **Read-aloud:** ready. "it" in "how it fooled us" = the line, named in the same sentence.

## 5. Summary pages (not recorded)

- **t32**, table "Which method when", row "Letters instead of numbers": BEFORE "Algebra, or plug in numbers that fit the
  figure and check the choices." → AFTER "Algebra, or plug in numbers that fit the figure and check every choice. Out of
  time? The first match is a reasonable guess." (her g071 tip; "check every choice" keeps the English warning that one
  match alone isn't proof). Built with `python3 summary_pages.py 32` → ~/Downloads/Topic-32-Summary-Page.html (7 math
  checks pass); looked at the PNG: the row wraps to two lines, nothing overflows, still one page.
- **t31**: nothing to remove. summary_pages/t31.json (and the built page, and content/full-course/topics/t31.json) have
  no √2 ≈ 1.4 / √3 ≈ 1.7 anywhere. Those decimals live only in the old summary VIDEO script r26-t31-summary-2 (t31.py
  lines 1329-1330 and 2495-2496), which the page replaced and which is not in the video ledger. Rebuilt anyway with
  `python3 summary_pages.py 31` (10 checks pass). Note `summary_pages.py` takes one topic per run, so "31 32" was run
  as two commands.

## Checks
- Spec runs `_ai_vis_t33.py`, `_ai_vis_t51.py`, `_ai_vis_t52.py` (all videos): no PROBLEMS. (A first draft of geo-079
  said "about three point one four"; the spec's decimal-estimate check flagged it, so it now gives the digits.)
- Private builds only: scratchpad/hr-geo/test.html and hw.html (AI_HANDWRITE=all), both exit 0, rebuilt after the fixes.
- `SRC=<test> python3 ai_check.py geo-079 solve-geo33-g090 solve-geo33-g092 solve-pt-q16 ch52-change`: all OK on both
  builds (notes only: "three hundred sixty", as before).
- `math_check.py 33`, plain and AI_HANDWRITE=all: PROBLEMS 0, WARNINGS 0, LAYOUT 0 (195 slides). math_check does not
  cover topics 51/52, so `layoutcheck.py` was run on solve-pt-q16 and ch52-change: 0 problems on both builds.
- Frames of every changed slide from the handwriting build (scratchpad/hr-geo/fr/ and fr2/), looked at. Fixed after
  looking: g092 slide 1 second row column ran off the slide (rows put in one column, figure enlarged); q16 slide 2 rows
  moved up off the "not drawn to scale" note. No early results; cues are substrings of their lines.
- Prompter dump: scratchpad/hr-geo/prompter.txt.

## Proposals for recorded videos
None. All five videos are unrecorded. (Optional, teacher's choice as before: solve-geo31-g071 is recorded; her
"first match is a reasonable guess" now lives on the t32 summary page instead.)

## Needs Claude
- **g089 not changed** (as instructed). It still needs 3.14 < π < 3.15 with 16 × 0.14; geo-079 now gives 3.14159…, so
  the bound is no longer untaught, but her one-step "move the decimal point" (10π → 31.4) still doesn't work with 16π.
  hebrew-vs-english-t33.md item 2 has a number proposal (8π, ring 84π → 20π ≈ 62.8) for the teacher.
- **Prompter display** (`_codex_reading_display_20261012.json`, not edited): the entries for solve-geo33-g090,
  solve-geo33-g092 and solve-pt-q16 have stale `paras` (re-rendered automatically). Wrong maths shown:
  - g090 2.0: "15² − 12² = 15 − 12 × 15 + 12" should be (15 − 12)(15 + 12).
  - q16 0.6: "1/2, times π over 2 − 2" should be ½(π/2 − 2); "π over 4 − 1" → π/4 − 1; "π over 2 − 1" → π/2 − 1
    (same in 2.4 "π/2 − 1" is fine, 2.7 "π over 2 − 1" → π/2 − 1).
  - g092 2.2: "3/4 = 3 × 1½ π" reads oddly ("three quarters is three times one and a half π") but is not wrong.
  - geo-079: the registry's scope_replacements for slides ≥ 4 look shifted by one slide (the "Why πr²" slide added on
    10-18), so "So the area, πr²…" is shown as "π r², … 3 × r²". Not caused by this change.
- t33_CHANGES.md / the student_review dumps still describe g090 as 12-35-37 and g092 as 6-14-15 (history files; not
  edited). The student-site question data comes from t33.py and is updated.
