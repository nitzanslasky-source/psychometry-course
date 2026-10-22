# Topic 52 (Charts & Tables): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/charts subtitles.rtf` (converted with textutil, 1,403 lines, all of it read). The same text is split
  into `studio-build/charts_src/seg01-seg11` (seg01-10 = her ten lessons, seg11 = her solutions of chart set 1). Line numbers below are
  in the converted RTF.
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t52.py`). Topic 52 is not
  in `base-v18.html`: its base translation is `studio-build/modulesV52a.py` (lessons) and `modulesV52b.py` (the three chart sets,
  from course book pp. 228-233, data changed).
- Recording status (`python3 video_status.py --list record`): **every topic-52 video is unrecorded**, all 29 of them (ch52-intro,
  -intro-2, -intro-3 are her camera parts; the other lessons and solve-ch-q01 … q15 are read in the Reading Studio). `--list send`
  lists none. So any restore costs no re-recording.

**Match scale.** As in the t23 report: SAME = same idea and every one of her methods (new numbers alone don't count; in her
lessons the English keeps her own numbers almost everywhere). CHANGED = same idea, different method, example or order. PARTIAL =
some of her content is missing (the cell says what). MISSING = no English equivalent.

**Her videos.** Ten lessons (מבוא, טבלה, נקודות, קווי, עמודות, קווי רציף, טווחים, מעגל, מצטבר, שינויים) and one solved set
(chart 1, the planets, 5 questions). Her subtitles have **no solutions for chart sets 2 and 3** (the car races and the weddings): the
set-1 file ends "בואו נמשיך לתרשים הבא", so the next sets were in the book only. Her Q4 appears twice in the subtitles (lines
1255 and 1299, identical, a copy error in the file, not two videos).

**How her videos map to the English ids.** Her intro → ch52-intro + ch52-intro-2 + ch52-intro-3 (one lesson read on camera in
three parts). Her range lesson (686-860) → ch52-range + ch52-regions (the regions part became its own video). Her pie/circle lesson
→ ch52-circle. Every other lesson is one-to-one. Her set-1 questions → solve-ch-q01 … q05 (same question types and answer positions,
new data; ch-q01's choices are reordered on purpose, so its answer is choice 2 where hers was choice 3).

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | מבוא – מבנה הסט · Intro: what a chart set is | 4-8 | A chart or table, then 4-5 questions; 5-6 minutes, a bit over a minute a question; first a minute to a minute and a half on the chart only; the skill: understand and analyse data shown in different forms | ch52-intro slide 1 | SAME (English adds why: every question uses the same chart) |
| 1b | "כל תרשים יכול להופיע" · The myth: any chart can appear | 9-19 | Wrong: the exam uses very specific types, all taught here; once in 1-3 years an odd one; 95% are these types | ch52-intro slide 2 | SAME |
| 1c | הוראות, הסבר ודוגמה · Instructions, explanation, example | 20-41 | Instructions say nothing special; an explanation, and almost always an example at its end; **the example is the most important thing**: check it in the chart; doesn't match → stop, reread slowly line by line; still unclear → leave the set, come back at the end of the section | ch52-intro slides 3-5, ch52-intro-2 slide 1 | SAME (English adds a worked check of the example on the bar chart, and a second sentence of our own) |
| 1d | הכותרות, היחידות וההערות · Titles, units, notes | 42-47 | Titles; units (thousands, units, hundreds, tens, percent); every note, "without it something won't add up" | ch52-intro-2 slide 2 | SAME (English adds 90 on a thousands axis, 40 on a percent axis) |
| 1e | סדר השאלות · Question order | 48-54 | Easy → hard; the last is harder or just longer; the first is usually a data pull; later ones calculation or deeper understanding | ch52-intro-2 slide 3 | SAME (English adds an example data pull, 2011 = 80 thousand) |
| 1f | טבלה מול תרשים, אקסל · Table vs chart, Excel | 55-66 | A table = rows and columns, a value at a crossing; a chart = data as a picture; Excel "insert chart": columns, line, pie; choose the chart that fits | ch52-intro-3 slides 1-2 | SAME (English adds a crossing example: 31-40 × siblings = 2.8) |
| 1g | מיקום התרשים בפרק; לא לדלג · Where the set sits; don't skip | 67-91 | Sets are placed by difficulty; the "always skip the chart" advice is a mistake: an early chart is easier than the questions around it (80% vs ~85% success); middle → solve it; end → you reach it anyway; an individual who is weak in charts may skip | ch52-intro-2 slide 4 | SAME |
| 1h | דיוק · Charts are drawn exactly | 92-100 | Unlike geometry figures, chart drawings are always exact; use them; many fast solutions are by eye (a sharper angle, a steeper line) | ch52-intro-3 slide 3 | SAME (English adds two conditions she uses later: check the scale, the units and any break first; compare steepness only on the same axes and the same time interval. The scatter lesson repeats "the chart is drawn exactly to scale") |
| 1i | יתרון הטבלה / יתרון התרשים · What each is good for | 101-126 | Table: many data about the same groups (siblings, children, friends, salary 6,200 → 8,300, rooms), focus on one and ignore the rest; a chart with that much data is noise. Chart: see a trend at a glance, where in a table you must read every number | ch52-intro-3 slides 4-5 | SAME (English makes the trend point concrete: salary 6,200/8,300/10,100 up, friends 12/9/7 down, "six numbers") |
| 1j | גרף הסימולציות · The practice-test graphs | 127-155 | Three shapes: (1) a big jump at first, flat from test 8-9; (2) almost nothing, a steep rise from test 4-5, flat from 10-11; (3) nothing until 7-9, then sharp; steeper = bigger improvement; (2) is the real picture, so don't worry if the first tests don't improve | ch52-intro-3 slides 3 and 6 | SAME (CHANGED order only: English shows shape 1 on the "exact drawing" slide and shapes 2-3 at the end) |
| 2a | הסקה מטבלה – בניית הטבלה · The car table, column by column | 175-206 | 2010: 60 thousand sold; "of them" = of all vehicles sold (45 private cars); private vs company ownership (40); commercial vehicles owned privately (4) | ch52-tables slides 1-3 | SAME (English adds "the 45 is part of the 60, not on top of it") |
| 2b | נושאים אחרים בתוך טבלה · Other topics inside a table | 207-214, 279-285 | Questions can bring in percents, averages, overlap, work, even motion; **so study charts after all the other problem types**; not every question is like that | ch52-tables slides 4, 10 | CHANGED: her study-order advice became "the good news is that we already know these topics". That is true in the English plan for the topics the lesson uses (23 percents, 24 overlap and 25 averages come before 52 in planData.ts; work 26 and motion come after it) |
| 2c | ממוצע · Average of the vehicles sold | 215-232 | 60+80+80+100 = 320, ÷4 = 80; then: no calculation needed, the numbers are symmetric (steps of 20, 0, 20), so the average is the middle | ch52-tables slides 5-6 | SAME |
| 2d | אחוזים · Percent of privately owned | 233-248 | "After the מ comes the whole"; 40/60 = 2/3 = 66⅔%; 50/80 = 5/8 = 62.5%; **reminder: 1/8 = 12.5% (half of 1/4), and know the multiples: 3/8 = 37.5, 5/8 = 62.5**; 65/100 = 65% | ch52-tables slides 7-8 | PARTIAL: everything except the multiples line. English derives 5/8 as 5 × 12½ but drops "3/8 = 37.5" and her "you must know the multiples too". The base (modulesV52a.py lines 643-644) had it |
| 2e | חפיפה · Overlap: private cars owned by a company | 249-278 | The squares method: private cars 45, privately owned 40, commercial + privately owned 4 → 40 − 4 = 36 → 45 − 36 = 9 thousand ("from here it's like sudoku") | ch52-tables slide 9 | SAME (the "sudoku" image is dropped) |
| 3a | נקודות על מערכת צירים · Points on axes, from the table | 289-337 | The most important type, the base of all others; axes (years; amount in thousands, 90 = 90,000); a key (black star, dot, white star, x); each point exactly at its value; visual advantage: up, same, up | ch52-scatter slides 0-4 | SAME |
| 3b | מספרים במקום סימנים · Numbers as markers (dealers) | 338-361 | A number at a point adds a variable (dealers); Q: greatest average per dealer: 60/5 = 12, 80/8 = 10, 80/10 = 8, 100/15 needn't be computed (< 10) → choice 1 | ch52-scatter slides 7-8 | SAME |
| 3c | ערכים שליליים · Negative values | 362-367 | An axis can go below zero (10,000 returned → −10); other charts, other stories | ch52-scatter slide 9 | SAME |
| 3d | שנתות קבועות; זיגזג · Equal steps; the Z break | 368-387 | Steps are equal and exact; an axis starting at 50 has a Z at the bottom: that gap is not to scale; nothing below it is shown (the x's are gone) | ch52-scatter slides 10-11 | SAME |
| 4a | גרף קווי – חיבור הנקודות · Line graph: join the points | 393-417 | The same chart with the points joined; remove the points; 4 identical lines → bold, dashed, dot-dash styles + the key | ch52-line slides 0-3 | SAME |
| 4b | לקו אין ערך · The line has no value between points | 418-430 | Only the measured points have values: no "2010 and a half = 70,000" | ch52-line slide 4 | SAME (English: "the bold line passes seventy there… no") |
| 4c | מגמה ושיפוע · Trend and slope; compare with points | 431-453 | The line shows trend: flat = no change, up = rise, a sharper angle = a bigger rise; with points alone it's hard to see which rise is bigger | ch52-line slides 5-9 | SAME (English adds numbers: a rise of 10 vs 15, and two equal rises of 20) |
| 5a | תרשים עמודות – מקווים לעמודות · Bars built from the lines | 454-497 | Same data as bars; build each series, shift each next to the other, update the key (white bar = sold); height = value (2010 privately owned = 40) | ch52-bar slides 0-2 | SAME |
| 5b | עמודה בתוך עמודה · A bar inside a bar | 498-510 | (1) 45 private cars inside the 60 sold. (2) **Inside the 40 privately owned, about 4 thousand are commercial, so what's left is private cars privately owned** | ch52-bar slide 3 | PARTIAL: example (1) only. Her second example, reading the remainder of an inner bar, is gone (the base had it, modulesV52a.py line 936) |
| 5c | חפיפה בעמודות · Overlap hidden in bars | 511-527 | 80 sold, 60 private, 50 privately owned: maybe all 50 inside the 60; push the 50 to the top → only 30 both; "if you haven't learned overlap, go back first" | ch52-bar slides 4-5 | SAME (English adds the calculation 60 + 50 − 80 = 30 and the conclusion "30 to 50". Her "go back to overlap" is not needed: topic 24 comes before 52 in the plan) |
| 5d | עמודות מצטברות · Stacked bars | 528-563 | Exclusive kinds (car / commercial / motorcycle) can be stacked; why: the dealer owner wants the total (~117-118 thousand in 2012); one kind = the gap (commercial 60 → 110 = 50); tailor the chart to the user (table, bars, a stack for the manager) | ch52-bar slides 6-7 | SAME (English adds that only the bottom part reads straight off the axis: private 2013 = 70) |
| 5e | עמודות לרוחב · Horizontal bars | 564-587 | Common on the exam and confusing; Carob/Zucchini, English 75 and 80; values on the x-axis; "turn your notebook 90°" | ch52-bar slide 8 | SAME ("turn the page in your mind") |
| 5f | סיכום עמודות · Bar recap | 588-597 | Know the nuances: horizontal, stacked, inside; check stacked/inside so commercial isn't read as 110 instead of 50 | ch52-bar slide 8 (end) | SAME |
| 6a | גרף קווי רציף – מעמודות לקו · Continuous line: from bars to a line | 598-623 | Website visitors, bars every 4 hours, strips = where most visitors are; example 16:00 = 390, forum; measure every hour, quarter hour, minute → one area → a continuous line | ch52-continuous slides 1-2 | SAME |
| 6b | לכל נקודה משמעות · Every point is a measurement | 624-645 | Unlike the line graph, every point on the line has meaning; temperature; the cars were yearly sums (daily sales would be continuous) | ch52-continuous slide 3 | SAME (English adds a reading at 12:30) |
| 6c | גידול יחסי · What relative increase means | 646-653 | Relative = compared with before, "times 1, 2, 3, 1.5…"; the bigger the multiple, the bigger the relative increase | ch52-continuous slide 4 | CHANGED: English explains it as "what fraction of the start was added" (100 → 150 = half more; 400 → 450 = an eighth more), instead of her "how many times". Her "times" wording returns in the question (80 × 4 = 320) |
| 6d | השאלה: הגידול היחסי הגדול ביותר · The question | 654-685 | 9:00: 80 → 300 (100 → 300 is ×3, so from 80 almost ×4); 15→16, 20→21, 23 small; don't compute every point, mark the slope before each hour; caveat: depends on the level, compare points at a similar level; choice 1 | ch52-continuous slide 5 | SAME (the caveat is kept: "compare the same interval, and check the starting value too") |
| 7a | תרשים טווחים · Range chart (rents) | 686-711 | The exam loves min-max; rent by rooms; the Z (0-2 not to scale); bottom = lowest, top = highest, bold line = mean; 6 rooms 4,500 / 8,000 / 6,500 | ch52-range slides 0-2 | SAME |
| 7b | הממוצע לא באמצע · The mean is not the middle | 712-722 | Higher than the middle = more expensive flats pull it up; one flat at 2,500 and the rest at 4-4.5 | ch52-range slide 3 | SAME (English shows it on the 2-room bar: middle 3,500, mean 4,000) |
| 7c | אלה ודניאל · Ella and Daniel (sample question) | 723-781 | שוכר/משכיר (a Hebrew-usage aside: who pays, who gets); Ella: max 7,500 − 2,500 = 5,000, min 4,500 − 4,500 = 0; Daniel: 7,000 − 2,000 = 5,000, 4,000 − 4,000 = 0; differences 0, 2,500, 5,000 possible; 5,500 impossible | ch52-range slides 4-5 | SAME (the language aside is adapted to English "rent / rent out") |
| 7d | אותו מידע בטבלה · The same data as a table | 782-818 | Three numbers per cell, the place gives the meaning (top left min, centre mean, bottom max) — common on the exam; a table makes adding cities easy, a chart gets noisy but compares by eye | ch52-range slides 6-8 | SAME (English adds "so always read the note" and a 4-room reading) |
| 8 | תרשים שטחים · Regions chart (health insurance) | 819-860 | Ranges as areas; height × weight, cost in thousands (4 = 4,000; 4-12 thousand); the example 100 kg, 174 cm → the striped area 6 → 6,000 | ch52-regions slides 0-2 | SAME (English adds a second person, 80 kg / 190 cm → 4,000) |
| 9a | תרשים מעגל – קריאה · Circle chart: how to read it | 861-884 | Common, different-looking; the website story again; hours round the circle, circles = visitors, dark areas = where most are; 9:00 = 300, forum | ch52-circle slides 0-2 | SAME |
| 9b | מערכת צירים מעוקלת · Bent axes, same as the continuous chart | 885-922 | Every chart so far except the table was on axes; here the axes are bent; points, bars or a line can sit on it; side by side with the continuous chart: 12:00 ≈ 320, 12-16 explanations | ch52-circle slides 3-4 | SAME |
| 9c | השעה המאוחרת בתרגול · Latest hour in practice | 923-960 | Looks like 20:00, but dark = most (more than half), not all → cannot be known | ch52-circle slide 5 | SAME (English adds 160 of 300 to show "most") |
| 9d | לחתוך ולפרוס · Cut it and unfold it | 961-969 | Cut at the top and unfold → the same chart on straight axes | ch52-circle slide 6 | SAME |
| 10a | גרף מצטבר – ההגדרה · Cumulative graph | 970-1019 | Each point = the sum up to it; a month = this point minus the previous; Pixeltech, thousands; example May = 20 but the point is 70; April 50; the bank account (10, 20, 50, 50, 70) | ch52-cumulative slides 0-3 | SAME (English adds March = 50 − 20 = 30) |
| 10b | ללא הכנסות · No income | 1020-1031 | A flat line: up to March 50, up to April 50 → April | ch52-cumulative slide 4 | SAME |
| 10c | סך ההכנסות · Total income | 1032-1049 | Don't add the months: the last point, 80 thousand, is "up to June", not June | ch52-cumulative slide 5 | SAME |
| 10d | נדיר, אבל להכיר · Rare, but know it | 1050-1060 | Not common; better to meet it before the exam | ch52-cumulative slide 5 (end) | SAME |
| 11a | גרף שינויים – ההגדרה · Change graph | 1061-1078 | Very rare but unusually hard, so we learn it; the values are changes; **ignore the line, look only at the points** | ch52-change slide 0 | SAME |
| 11b | הדוגמה והחלק המבלבל · The example; the confusing part | 1079-1096 | Week 2 = +10 (100 → 110); the line goes down into a point of +5, which is a rise | ch52-change slides 1-2 | SAME |
| 11c | כמה שבועות ללא שינוי · Weeks with no change | 1097-1121 | Remove the line; points at 0 = weeks 5, 9, 10 → 3; bring the line back: into 5 it looks like a drop, into 9 like a rise | ch52-change slides 3-4 | SAME |
| 11d | 75 מתנדבים · 75 at week 2, how many at week 6 | 1122-1160 | +5 → 80 (though the point is lower); **week 4: the line is flat, it looks like no change, but +5 → 85**; week 5: looks like a drop, 0 → 85; −10 → 75; recap "here the line is flat but it's a rise, here it goes down and there's no change"; choice 1 | ch52-change slide 5 | PARTIAL: the calculation is all there, but the step-by-step "the line lies" commentary is cut to nothing: week 4's flat line, which hides a rise, is never pointed out (English: "Week four is plus five again"), and neither is her recap. "A flat line can be a rise" is the one form of the trap that no English video shows, though the summary page states it. The base had both (modulesV52a.py lines 1599-1601) |
| 11e | סיום הנושא · Topic close | 1161-1180 | Confusing, rewatch it if needed; rare; "the types on the exam are very clear, exactly these; very rarely another; go through these lessons and you're ready" | ch52-change slide 5 (end) | PARTIAL → effectively MISSING for the topic close: English keeps "watch this video again if you need to" and "remember the one rule", then "That's the last type of chart. Next, we'll solve full chart sets." Her closing reassurance (back to the intro's "95%") is gone; the base had it (modulesV52a.py line 1614) |
| 12 | שאלה 1 – פחמן מעל 60% · Q1 carbon above 60% | 1181-1206 | Draw a boundary line (in your head or on the chart), count to the right; trap: under pressure checking hydrogen 60% gives 1, not a choice → stop, check the key and what was asked; each shape counts at its centre | solve-ch-q01 | SAME (English adds the trap of the ring touching the line, counted at its centre = choice 1; and reads the page and checks one shape first, since this chart has no example) |
| 13 | שאלה 2 – הכי מתאים למגורים · Q2 best for living | 1207-1229 | Don't check every sample; high carbon = right, low hydrogen = bottom → the overlap of the two areas, one sample | solve-ch-q02 | SAME (English adds why Mercury is out: far right but high) |
| 14 | שאלה 3 – הטווח הגדול · Q3 largest carbon range | 1230-1254 | Leftmost to rightmost per planet; draw a line, don't read and subtract; compare lengths and rule out; "one of the main ways we solve chart questions" | solve-ch-q03 | SAME |
| 15 | שאלה 4 – נכון בהכרח · Q4 necessarily true | 1255-1342 | Before checking choice 1, read all the choices: the same idea (direct / inverse relation); one planet jumps out as a straight rising line; then check each planet in detail (up, down, up = not steady) | solve-ch-q04 | SAME (both ways; English adds "one exception is enough") |
| 16 | שאלה 5 – תרשים קטן · Q5 which mini-graph | 1343-1403 | Circle "hydrogen"; the mini-graphs are taken from the main chart; don't check graph by graph, rule out where they differ; start at the edges (below 10%: the count rules out two; the middle would need two lines; then the other edge, above 60%: one) | solve-ch-q05 | SAME (English adds that graph 1 is what counting carbon gives) |

**Count by row (55 rows: 1a-1j, 2a-2e, 3a-3d, 4a-4c, 5a-5f, 6a-6d, 7a-7d, 8, 9a-9d, 10a-10d, 11a-11e, 12-16):**
SAME 49 · CHANGED 2 (2b, 6c) · PARTIAL 4 (2d, 5b, 11d, 11e) · MISSING 0.
(11e is counted as PARTIAL because its "rewatch it" line survives; its main point, the topic-closing reassurance, is missing.)

### Count by video (her 15 units)

| Unit | Match |
|---|---|
| Intro (1a-1j) | SAME (order of the simulation graphs changed only) |
| Tables (2a-2e) | PARTIAL (the 3/8 = 37.5 multiples line was cut; the study-order advice changed) |
| Points on axes (3a-3d) | SAME |
| Line graph (4a-4c) | SAME |
| Bar chart (5a-5f) | PARTIAL (the second bar-inside-a-bar example was cut) |
| Continuous line (6a-6d) | CHANGED (relative increase is explained as a fraction added, not "how many times") |
| Range + regions (7a-8) | SAME |
| Circle (9a-9d) | SAME |
| Cumulative (10a-10d) | SAME |
| Change graph (11a-11e) | PARTIAL (the week-4 "flat line, yet a rise" point and the topic-closing lines were cut) |
| Q1-Q5, chart set 1 | SAME (5 units) |

**By video: SAME 11 · CHANGED 1 · PARTIAL 3 · MISSING 0** (15 units).

---

## 2. English → Hebrew (English topic-52 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| ch52-intro slide 5 (part) | A worked check of the example on the bar chart, plus one sentence of our own (2013 = 100 thousand) | none (she only describes the check) | no |
| ch52-scatter slides 5-6 | The "draw a line at the value and count past it" tool (more than 50 privately owned → 1 year; "on the line is not more"; more than 70 sold → 3; the line can stand up) | the tool is hers, from set-1 Q1 (1181-1206); here it is taught in the lesson first | no |
| ch52-line slides 6-7 (part) | Steepness checked in numbers (rise 10 vs 15; two equal rises of 20) | none | no |
| ch52-bar slide 5 (part), slide 7 (part) | The 60 + 50 − 80 = 30 calculation and "30 to 50"; only the bottom part of a stack reads off the axis | none | no |
| ch52-continuous slide 4 (part) | Relative increase with numbers (100 → 150 vs 400 → 450) | replaces her "times" explanation (row 6c) | no |
| ch52-regions slide 3 | A second person read off the chart (80 kg, 190 cm → 4,000) | none | no |
| ch52-practice-intro (whole video) | How to attack a set: a minute on the page, check the example, axes / units / key / notes; each question stands alone; circle the key word; answer not among the choices → stop and check; solve by eye, calculate only when you must | collected from her intro and her Q1/Q5 tips; "each question stands alone" is new | no |
| solve-ch-q06 … q10 (chart set 2, car races) | 5 questions: a place from a prize (q06), counting dramatic changes ("three or more", q07), the average prize by calculation and by the balance (q08), skip places 6-7 (q09), the same total / same teams → same average (q10) | none in her subtitles (book pp. 228-233 questions only, no video) | no |
| solve-ch-q11 … q15 (chart set 3, weddings) | 5 questions: shared guests belong to both sides (q11, q12), 1% must be a whole person (q13), percent × bar (q14), the weighted average by calculation and by the seesaw (q15) | none in her subtitles | no |
| ch52-summary | Not read; replaced by the summary page summary_pages/t52.json | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **The change graph, week 4: "the line is flat, so it looks like no change, but the point says +5, so it's a rise"** (and her recap: flat can be a rise, down can be no change) | ch52-change slide 5, at "Week four is plus five again" (2 sentences) | no | **Restore.** It is the second form of the graph's one trap, she makes a point of it, and the summary page already states "flat can be a rise", a case no English video shows. The base translation had it |
| 2 | The second bar-inside-a-bar example: inside the 40 privately owned, about 4 thousand are commercial, so the rest (36) are private cars privately owned | ch52-bar slide 3, after the 45-of-60 example (2-3 sentences) | no | Optional. It practises reading the remainder of an inner bar (the same skill as the stacked "gap" trap), and it links back to the 36 of the tables lesson |
| 3 | The fraction multiples: 3/8 = 37.5%, 5/8 = 62.5% ("know the multiples too") | ch52-tables slide 8, after "an eighth is twelve and a half percent" (1 sentence) | no | Optional. The fraction table is taught in topic 23 (wp-052-2); here it is only a reminder |
| 4 | The topic close: "the chart types on the exam are very clear, exactly the ones we learned; very rarely something else; go through these lessons and you're ready" | end of ch52-change slide 5, or the start of ch52-practice-intro (1-2 sentences) | no | Optional. It closes the loop on the intro's 95% promise; there is no teaching content |
| 5 | Her advice to study charts after all the other problem types | — | — | Not needed. The plan (planData.ts) already puts topic 52 after percents, overlap and averages, which are the topics the lessons use |
| 6 | "If you haven't learned overlap, go back first" | — | — | Not needed, for the same reason (topic 24 comes first) |

**Wrong compared with her: nothing found.** I checked the numbers that move between lessons against modulesV52a.py (stacked bars:
2011 commercial = 80 − 55 = 25, and 2012 = 110 − 60 = 50; cumulative: March = 50 − 20 = 30), and they agree. The change of answer
position in ch-q01 (choice 2, hers was 3) is deliberate (`_t52_reading.py` REORDER), and the script names the new position correctly.
Small softenings, none wrong: "charts are always exact" became "we can read values from the drawing, but first check the scale"
(row 1h); "the line has no value between points" is scoped to "in this yearly chart" (row 4b).

Every topic-52 video is still unrecorded, so all four candidates can go in without re-recording.
