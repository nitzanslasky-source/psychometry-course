# Topic 27 (Motion): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed. This is also the checklist for the writers of the new
topic-27 reading scripts.

- Hebrew source: `~/Downloads/02-Word-Problems-Original-Subtitles.txt`, lines 6984-8288 (all of it read).
- English: the per-topic dump `scratchpad/ext/course/t27.txt` (every video's spoken text) and `q27.txt` (questions), checked
  against `studio-build/base-v18.html` and `math_patches/t27.py` where the numbering or the practice set needed explaining.
- Recording: topic 27 has no reading scripts yet (only `ai_scripts/r26-t27-summary.json`) and none of its ids is in any
  `video_status.py` list, so **nothing in topic 27 is recorded**. Every target below is unrecorded.

**Match scale** (as in the t23 report): new numbers alone are not a change. SAME = same idea and all her methods. CHANGED =
same idea, but a method, the example type or the order differs. PARTIAL = some of her content is missing. MISSING = none.

**Her method names in English.** יחסים זהים → "identical ratios"; ערך משולש → not named in topic 27 English; הצבת מספרים →
"plugging in (friendly) numbers"; הצבת תשובות → "plugging in the answers"; הברקה → "insight"/"the spark of insight"; her
"אילו" (what-if) elimination → "imagine X were exactly twice as fast" (the name is not used); משולש התנועה → "the triangle";
"תן למסכן" (give to the poor one, from topics 22/26) → not used by name (g121 just says the fast one covers one extra lap).

**The id numbering (106-121) has no real gaps.** Her items: 106 intro lesson, 107 walker example, 108 plane (Pythagoras), then
the average-speed lesson that runs on in the same video after the plane (no break in her subtitles) → English split it off as
**wp-108-after**; 109 Dimona, 110 speed-ratios lesson, 111 Dani/Dina, 112 Yaron/Moti, 113 relative-speed lesson, 114 Shimon/Roi,
115 truck, 116 Miki, then "לימוד מתקדם" + 117-121. Lessons have wp- ids, questions solve-wp27-gNNN.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1 | מבוא לתנועה · Intro: distance, speed, time | 6985-7039 | Motion = a work problem (seeds 20/hour ↔ 20 km/hour); d = t × v, cover-the-letter triangle ("know it cold, fine; need the triangle, here it is"); 30 kph × 4 h = 120; same units always; 1 km = 1000 m, 1 m = 100 cm, 1 h = 60 min, 1 min = 60 s; kph / m/s meaning; ×3.6 rule: forget it (almost never on the exam; nobody remembers multiply or divide) → identical ratios | wp-106 slides 1-5 | SAME (18 × 2 = 36; the unit facts are on the slide, without 1 m = 100 cm). English adds: minutes as fractions of an hour, "1.25 h is 1 h 15 min", the speed-distance-time table (slide 6) |
| 2 | דוגמה: הולך רגל 5 מ'/ש' · Walker 5 m/s, km in half an hour | 7041-7076 | Identical ratios: 1 s → 1 min (×60) → 300 m; → 30 min (×30) → 9000 m = 9 km. "Better than memorising 3.6" | solve-wp27-g107 (scooter 6 m/s, 50 min → 18 km) + the worked example on wp-106 slide 5 (8 m/s, 25 min) | SAME (English adds the trap 300 m = mixing seconds with minutes). Note: English teaches it twice, see §2 |
| 3 | פיתגורס: מטוס ממריא · Plane takes off, 300 kph, 1 min, horizontal 4 km | 7077-7116 | Convert to 1 minute (÷60 both) → 5 km along the path; sketch, drop a perpendicular, 3-4-5 → height 3. Also: someone walking north and someone west = Pythagoras; whenever directions differ, draw; in motion always draw | wp-106 slide 7 (Draw a sketch) + solve-wp27-g108 (gondola 17 kph, 6 min, 1.5 km → 0.8) | SAME (8-15-17 in tenths of a km, plus the full Pythagoras for those who don't know the triple) |
| 4 | מהירות ממוצעת · Average speed (lesson) | 7117-7147 | The hand across the notebook (slow, fast, slow); = one constant speed for the whole trip; total distance ÷ total time; NOT the average of the speeds; rare on the exam, but it hides in "if it had moved at a constant speed" | wp-108-after slides 1-4 | SAME. English adds: stops count as time; equal TIMES → the plain average is right (60 and 90 → 75); "first ask: equal distances or equal times?" |
| 5 | דימונה–באר שבע 60/40 · There at 60, back at 40 | 7149-7204 | Not 50: logic first (less time at 60, so closer to 40; weighted-average reminder); no formula / weighted average; distance missing → plug in 120 (divides by both) rather than x; 240/5 = 48; "very rare on the exam" | solve-wp27-g109 (105 / 70 → 84) | SAME (logic → eliminate 90 and 87.5, plug in 210). English adds Method 2, algebra with d, which also shows why plugging in works |
| 6 | יחסי מהירויות · Speed ratios (lesson) | 7206-7242 | Some questions need no calculation; ratios run through the whole quantitative section; same as work: time fixed → v and d direct; speed fixed → t and d direct; distance fixed → t and v inverse; the skill is spotting when to use them | wp-110 slides 1-5 | SAME (English adds the speed numbers 3:4 → 4:3). English adds "What is fixed?" (4 quick situations) and "Two things change? The V" |
| 7 | דני ודינה פי 1.5 · Dani and Dina meet, she is 1.5× faster | 7244-7365 | (1) Ratios: 1:1.5 = 2:3, same time → distances 2:3, whole = 5 parts → 2/5. (2) Plug in numbers: 10 and 15 (×10 to drop the decimal), meet after 1 hour → 10/25. (3) "אילו" elimination: he covers less than half (out 2/3); if she were 2× → 1/3, she is slower than that → more than 1/3 (out 1/3, 1/4) | solve-wp27-g111 (Theo 1.25× → 4/9) | SAME (all three methods, in her order; 16 and 20, 1 hour; "imagine Theo were exactly twice as fast"). Her aside "plugging in works in other topics too, even geometry" is not said |
| 8 | ירון ומוטי פי 2.5 · Yaron and Moti, Tel Aviv–London | 7368-7440 | Not a meeting: Moti flies the whole way. 1:2.5 = 2:5, whole route = 5 parts (not 7) → 2/5. Plug in 10 and 25, 1 hour → the route is 25 → 10/25. Summary: meeting vs one covers everything; same time → distances follow speeds | solve-wp27-g112 (rowboat / motorboat 4.5× → 2/9) | SAME (both methods; "Two elevenths would be a meeting question" keeps her 5-not-7 contrast) |
| 9 | מהירות יחסית · Relative speed (lesson) | 7442-7498 | Rate the gap closes/opens; opposite directions (towards or apart) → add (truck 20 + car 50 = crash at 70); same direction → subtract; only the gap between them matters, not the whole road | wp-113 slides 1-5 | SAME (walkers 3 and 5; chase 9 and 6). English adds "one leaves earlier → work out the head start first" and the sketch with the gap marked |
| 10 | שמעון ורועי · Shimon and Roi walk apart, 6 and 4 kph, 500 m | 7501-7528 | Apart → add: 10; 500 m = ½ km (same units); ½ ÷ 10 = 1/20 h (tip: expand by 2, not 10) → 60/20 = 3 min | solve-wp27-g114 (8 + 10, 1.8 km → 6 min) | SAME (English adds the trap 10 minutes). Her "expand by 2" tip doesn't apply to the new numbers |
| 11 | משאית אשדוד–חיפה · Truck 6:00 at 80, car 6:30 at 100, 130 km | 7531-7575 | Stage 1: truck alone ½ h → 40 km, 90 left. Stage 2: towards each other → 180; the distance in the table is always the gap between them (meeting or chase); 90/180 = ½ → 7:00. Always draw, even do the calculation on the sketch | solve-wp27-g115 (bus/car, 204 km → 10:20) | SAME |
| 12 | מיקי ואביו · Miki leaves at 4 kph, father catches him after ½ h more | 7578-7643 | Head start ¼ h → 1 km gap; the common mistake: only the starting gap counts; 1 ÷ ½ = 2 = how much FASTER the father is, not his speed (at 2 he'd never catch him) → 6. Closing recap of the lesson: add / subtract; chases are where students slip; "Miki could be 100 and the father 102, only the gap matters" | solve-wp27-g116 (Zoe 15, Sam after 12 min, 20 min → 24) | SAME (all steps, "at nine he'd never catch her"; the recap is in wp-113 slide 5). Her "100 and 102" line is not there. English adds Method 2 (both cover 8 km) |
| 13 | לימוד מתקדם · "Advanced learning" heading | 7647 | One heading line, no teaching | the section "Further guided examples" + "Advanced motion." at the start of g117-g121 | SAME |
| 14 | 8 ק"מ ב-10 דק' / 10 ק"מ ב-8 דק' · Car A 8 km in 10 min, car B 10 km in 8 min, difference in kph (easy+) | 7648-7764 | (1) Calculation: minutes → hours (÷60, shown with 30/60 = ½), 8 ÷ 1/6 = 48, 10 ÷ 8/60 = 75. Two mental-subtraction tips for 75 − 48: add 2 to both (77 − 50); walk via a round anchor (48 → 50 → 75). (2) Ratios, her recommended way: 10 → 60 min is ×6 → 48; for B, three ways to see 8 → 60: ×7.5, or "+2 is a quarter of 8, so add a quarter of 60" → 75, or (if you don't see it) the triangle value | solve-wp27-g117 (9 km / 15 min vs 15 km / 9 min → 36 and 100, 64) | CHANGED: the calculation and both subtraction tips are kept (add 4 to both; walk via 40), and ratios is still "the one I recommend". But with 9 minutes her three ways for the awkward one are replaced by one new step (÷3: 5 km in 3 min, ×20). **Her fallback "if you don't see the ratio, use the triangle value" is gone** |
| 15 | האומגה 120 מ' ב-10 שניות · Zip line, double speed to the middle, then half speed | 7766-7861 | Instinct says 10, wrong. (1) Calculation: 12 m/s; 60/24 = 2.5 (tip: know 60 = 5×12), 60/6 = 10 → 12.5. (2) Ratios: normally 5 + 5 s; double speed → half time 2.5; half speed → double 10. (3) Insight: the slow half alone = 10 = the whole normal trip, plus something → eliminate 10, 7.5, 5. Recommended: ratios; insight only if you see it | solve-wp27-g118 (elevator 60 m / 20 s → 25) | SAME (all three methods and her verdict "Ratios. The insight is great if you happen to see it"). The "60 = 5×12" tip doesn't fit the new numbers |
| 16 | גבריאל ואלכסנדר, B אמצע הדרך · B is the midpoint; one at 30 the whole way, the other 30 min to B then 20 kph | 7863-7963 | (1) Algebra with a d-t-v table: call each half x (not x/2) → 2x/30 = ½ + x/20; stay in hours ("½, not 30"); Alexander's speed on the first half isn't needed; x = 30 → the whole road is 60. (2) Plug in the answers: start with the round ones (60 or 90), 60 first because halves are 30 not 45 → 2 h = ½ + 1½ ✓. "Not by chance: NITE checks whether you know what to plug in first" | solve-wp27-g119 (48 kph; 20 min then 36 kph → 48) | SAME (x for each half, "stay in hours", plug in the friendliest answer first, "Not luck"). English adds the trap 24 = only x. Her line "you could compute his first speed but you don't need it" is not said (minor) |
| 17 | פרטוריה–קייפטאון · 1,600 km in 6 h, new train 50% faster | 7965-8059 | (1) Calculation: v = 1600/6 = 800/3, **left as a fraction on purpose** (it cancels later); +50% = ×1.5 (100 → 150) → 400 → 4 h. (2) Ratios: 2× faster → ½ the time, 3× → ⅓, so 1.5× → ÷1.5 → 4. (3) Insight/estimation: if it were 2× → 3 h, so out 3 and anything under 3; 9 h is slower than the old train → out; three choices gone with one easy number. Recommended: ratios, insight for those who see it | solve-wp27-g120 (ferry 360 km / 12 h, 60% faster → 7.5) | CHANGED: methods 1 and 2 are the same ("adding sixty percent means multiplying by one point six"; ÷1.6). Method 3 still starts from "twice as fast → 6 h" and "slower than the old ferry is impossible", but with these choices it leaves two (8 and 7.5), so English adds a second easy number (×1.5 → 8 h, so less than 8). Her point "one easy number kills three choices" becomes two steps. Her "leave the speed as a fraction" tip is lost because the new speed (30) is whole |
| 18 | קרטינג במסלול מעגלי · Karts on a 500 m circular track, 60 and 50 kph, time between consecutive meetings (medium+/hard) | 8061-8283 | First the meaning, with the animation (red 5 laps, blue 6): consecutive meetings = the fast one gains one full lap; **it doesn't have to be counted from the start: any two meetings in a row**; "or 'when it laps it', depends on the wording, same meaning". (1) Algebra: same t, 60t = 50t + ½ ("give to the poor one": add the lap to the slower), ½ km (units), t = 1/20 h = 3 min; "this is not how we solve it on the exam". (2) Relative speed: chase → subtract → the slow one stands still, the fast one moves at 10; 10 km in 60 min, ½ km → ×6 → 3 min | solve-wp27-g121 (400 m track, 12 and 9 → 8 min) | PARTIAL: the meaning of consecutive meetings, "you stand still", subtract, and the algebra are all there (English puts the relative-speed way first and the algebra second as a check, which matches her "not how we solve it on the exam"). **Missing: "consecutive meetings can be any two in a row, not only from the start" and "'laps it' / 'gains a full lap' is the same question in other words"** |
| 19 | 20 שאלות תרגול עצמי · 20 self-practice questions (no video) | 8286 | — | wp27-p01 … p20 in the practice section (p10 moved to T33 as the central-angle version; its motion version was removed as a repeat of the circular-track idea, which is covered by q-r26-t27-03) | SAME |

**Count by row (19 rows):** SAME 16 · CHANGED 2 (14, 17) · PARTIAL 1 (18) · MISSING 0.

### Count by video (her units)

| Unit | Match |
|---|---|
| Intro lesson (1) | SAME |
| Walker example (2) | SAME |
| Plane / Pythagoras (3) | SAME |
| Average-speed lesson (4) | SAME |
| Q Dimona (5) | SAME |
| Speed-ratios lesson (6) | SAME |
| Q Dani/Dina (7) | SAME |
| Q Yaron/Moti (8) | SAME |
| Relative-speed lesson (9) | SAME |
| Q Shimon/Roi (10) | SAME |
| Q truck (11) | SAME |
| Q Miki (12) | SAME |
| Advanced heading (13) | SAME |
| Q cars 8/10 vs 10/8 (14) | CHANGED (her ratio paths for the awkward car, and the triangle-value fallback, replaced) |
| Q zip line (15) | SAME |
| Q B midpoint (16) | SAME |
| Q Pretoria (17) | CHANGED (estimation now needs two steps; "leave it as a fraction" lost) |
| Q karts (18) | PARTIAL ("any two meetings in a row" / "laps it" wording missing) |
| 20 practice questions (19) | SAME |

**By video: SAME 16 · CHANGED 2 · PARTIAL 1 · MISSING 0.**

---

## 2. English → Hebrew (English topic-27 parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| wp-106 slide 3 (part) | Minutes as fractions of an hour (20 = ⅓, 40, 12, 45); 1.25 h ≠ 1 h 25 min | none as a rule (she converts inside the questions) | no |
| wp-106 slide 5 (part) | A worked example of the identical-ratios conversion (8 m/s, 25 min) **inside the lesson**, and then g107 does the same thing again | her lesson said "we'll see an example in a moment" and the example WAS the next video (item 107) | no |
| wp-106 slide 6 | The speed-distance-time table (rows = people or parts, totals add distances and times, never speeds; "find the link") | only implicit ("נציב בטבלה" inside her questions) | no |
| wp-108-after slides 3-4 (parts) | Stops count as time; equal times → plain average; "equal distances or equal times?" | none | no |
| wp-110 slide 6 | "What is fixed?" – four quick situations | none (her "the skill is spotting when") | no |
| wp-110 slide 7 | "Two things change? The V" (table V with distance in the middle) | none in motion (the V is from the work topic) | no |
| solve-wp27-g109 slide 2 | Method 2, algebra with d | none (she said "x is possible but why?") | no |
| solve-wp27-g116 slide 2 | Method 2, both cover the same 8 km | none | no |
| every solution | a named trap choice | none | no |
| r26-t27-special + solve-q-r26-t27-01/02/03 | Train with a length; boat on a river (current = half the difference); circle, opposite directions (add, one lap together) | none | no |
| r26-t27-graphs + solve-q-r26-t27-05/06 | A percent faster → flip the fraction for the time; letters in the choices (plug in, algebra, unit count) | none (Pretoria touches "% faster") | no |
| r26-t27-summary | Spoken summary (her "בואו נמשיך לסיכום" summary is not in the subtitles) | her summary video exists but not in this file | script only |
| solve-q-r26-t27-31 | The V method, three times as far at 1.5× the speed | none | no |
| practice extras | wp27-p22, p24, p27, q-r26-t27-09/-10/-21/-22 | none | — |

**A repeat to consider cutting** (memory rule "teach in question videos; cut repeats, not content"): wp-106 slide 5 works a full
conversion example and g107, the next item in the flow, works the same conversion the same way. Her own order was "rule in the
lesson, the example in the next video". Cutting the three example lines from wp-106 slide 5 (keep "Forget 3.6… Instead:
identical ratios, the next question shows how") saves about 15-20 seconds and nothing is lost.

---

## 3. Missing from English: restore?

All targets are unrecorded (topic 27 has no reading scripts yet), so every restore is free.

| # | Her content | Where it would go | Length | Recommendation |
|---|---|---|---|---|
| 1 | **Karts: "consecutive meetings means any two meetings in a row, not only from the start"** and "'when it laps the other' / 'gains a full lap' is the same question" | solve-wp27-g121 slide 1, right after "It meets the slower one again exactly when it has gained one full lap" | 2 sentences, e.g. "And it doesn't have to start at the start line: any two meetings in a row are one lap apart. Some questions ask 'when does it lap the other one?' It's the same question." | **Restore.** It's about how the exam words the question, and that wording is exactly what confuses students (her words) |
| 2 | Cars question: "don't see the ratio? Use the triangle value" | solve-wp27-g117 slide 2, after the train step | 1 sentence: "Don't see it? Triangle value: fifteen times sixty, over nine — a hundred." | Optional. It's her safety net for anyone who can't spot the ratio; cheap |
| 3 | Pretoria: one easy number (×2) knocks out three choices | solve-wp27-g120 slide 3 | none if the choices are changed so that 8 isn't one of them (e.g. 6, 7.5, 9, 19.2 → "more than 6, less than 12" leaves 7.5 at once) | Optional. Only if the question's choices are being reworked anyway; the current two-step version is correct and still teaches the idea |
| 4 | Miki: "Miki could be 100 kph and the father 102, only the gap matters" | end of solve-wp27-g116 slide 1 or wp-113 slide 5 | 1 sentence | Optional. The point ("only the starting gap") is already said three times |
| 5 | Pretoria: leave the speed as a fraction (800/3), it cancels later | — | — | Not needed: the new speed (30) is whole, so the tip has nothing to work on |
| 6 | Dani/Dina: "plugging in friendly numbers works in other topics too, even geometry" | — | — | Not needed: general plugging-in is taught in the psychometric-thinking topic |
| 7 | Her name "תן למסכן" (give to the poor one) in the karts algebra | — | — | Not needed: the English course doesn't use the name in topics 22 or 26 either; g121 states the idea (the fast one covers one extra lap) |

**Nothing in English is wrong compared with her.** All the English numbers were re-checked (g107 18 km, g108 0.8 km, g109 84,
g111 4/9, g112 2/9, g114 6 min, g115 10:20, g116 24, g117 64, g118 25 s, g119 48, g120 7.5 h, g121 8 min, the wp-110 V = 60);
each of her methods still works with the new numbers, except the three cases in rows 14, 17 and the minor tips noted
(expand by 2 in row 10, 60 = 5×12 in row 15) whose numbers no longer apply.
