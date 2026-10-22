# Topic 26 (Work and rate / הספק): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/02-Word-Problems-Original-Subtitles.txt`, lines 5922-6983 (all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t26.py`), the base
  translation `studio-build/base-v18.html` (video ids and the original question stems), and the practice dump `ext/course/q26.txt`.
- Recording status from `python3 video_status.py --list record`: **every topic-26 video is still unrecorded** (wp-092, -2, -3,
  wp-094, -2, wp-097, -2, wp-099, -2, all solve-wp26-g093…g105b, solve-q-r26-t26-01/-02/-03/-04/-21, r26-t26-factors).
  `--list send` shows no topic-26 video. So every restore below is free (no re-recording).

**Match scale** (as in the t23 report). English questions use new numbers on purpose, so new numbers alone are not a change.
SAME = same idea and every one of her methods. CHANGED = same idea, but a method/step works differently or is lost because of
the new numbers. PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Her names carry over.** הספק × זמן = עבודה → "rate times time is equal to work"; משולש ההספק (עז"ה) → "the formula triangle"
(the Hebrew acronym is not translatable and is dropped); הספק משותף → "combined rate"; השוואת זמנים → "equal times / compare
both workers over the same number of hours"; שאלות צוות → "team questions"; שיטת ה-V → "the V method", V הפוך → "the V turns upside
down"; her order mnemonic "צוות, עבודה, זמן – צריך עוד זמן" → "**Teamwork takes time**" (same job, an English pun; her student
anecdote is not kept); זמן עבודה → "worker-hours / worker-days"; "תן למסכן" → "give it to the little guy"; אביבתיה → "Omarpriya";
the elephant-and-mouse joke and "Batya sits with a coffee" are both kept word for word.

**Numbering.** The ids follow her order with no gaps: 092 = lesson 1, 093 = her Yuval example (inside lesson 1 in Hebrew, a
try-first question in English), 094 = lesson 2, 095 = pool pumps, 096 = beer barrels (both inside lesson 2 in Hebrew), 097 =
lesson 3, 098 = her lesson-3 carpenters example (made a question), 099 = lesson 4, 100 = the road (inside lesson 4 in Hebrew),
101-105 = her five advanced questions, 105b = her sixth (the water tower). Her "לימוד מתקדם" (6403) is only a heading, not a video.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew · gloss) | Lines | What she teaches / every method | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | מבוא להספק – הנוסחה · Intro, the formula | 5923-5944 | הספק = what you get done in a unit of time; rate × time = work; 3 quantities, given two find the third; rate = work/time, time = work/rate | wp-092 slides 0-1 (baker 6 cakes/h × 4 h) | SAME |
| 1b | משולש ההספק (עז"ה) · The rate triangle | 5945-5963 | Work on top, time and rate below; "hide the one you want" and multiply/divide what is left; all three cases | wp-092 slides 2-3 (+ pump 150 L, printer 48 pages) | SAME (English adds two worked uses) |
| 1c | גידי – עבודה מול הספק · Gidi: work vs rate | 5964-5995 | 8 tequilas in 2 min: work 8, time 2, rate is NOT "4" but 4 per minute; a rate is always a fraction (4/1); students confuse work and rate; 8/2 = 4/1, write it either way | wp-092 slide 4 (45 bottles in 5 min, "nine bottles per minute") | SAME |
| 1d | יובל והנקניקיות · Yuval, x hot dogs in y min, rate ×2, time 3y | 5996-6033 | (1) Equal ratios: new rate 2x in y; y → 3y is ×3 so 6x; "or across the row, y → 2x is ×2, so 3y → 6x, either direction works"; time ×3 → work ×3. (2) Triangle value 3y·2x/y = 6x | solve-wp26-g093 (flyers, rate ×3, time 5y) | SAME (ratio table step by step, triangle value; English adds the formula and plug-in-numbers methods and the trap 8x = adding the factors). Minor: her remark that you can also go across the row is not said |
| 1e | יחס ישר / הפוך · Direct and inverse | 6034-6089 | Time fixed → rate and work direct (2 vs 4 hot dogs/min in 60 min); rate fixed → time and work direct (60 vs 30 min); work fixed → rate and time inverse (120 hot dogs: 60 vs 30 min); "intuitive, but keep it in mind for team questions" | wp-092-2 slides 2-4 (painter, walls) | SAME (English adds why: rate × time stays 12; "three times as fast takes a third of the time") |
| 2a | הספק משותף · Combined rate | 6091-6113 | Several workers, usually different rates; add the rates (3 + 2 exercises/min); a worker working against the others is subtracted (wash 5 plates, he dirties 2 → 3) | wp-094 slides 0-1, 3 (Dan/Noa 3 + 2, same plates example) | SAME (English adds slide 2 "never add the times", slides 4-5 "call the job one, fraction rates") |
| 2b | משאבות בבריכה · Pool: 2 pumps fill in 6 h, 1 empties in 9 h, from 8:00 | 6116-6162 | Rate = 1 pool/6 h = 1/6; the emptying pump gets a minus; 1/6 + 1/6 − 1/9 = 2/9; "2/9 means 2 pools in 9 hours" → 1 pool is half → 4.5 h (direct relation); add to the clock → 12:30 | solve-wp26-g095 (2 hoses 15 h, outlet 20 h, from 7 a.m.) | SAME (fractions, minus, "the fraction means pools in hours", clock time. With the new numbers the sum reduces to 1/12, so the "2 pools → halve" step is not needed here; it is taught in wp-094 slide 5: 2/15 → 7.5 h. English adds plug-in a pond size and the trap "forgot the outlet") |
| 2c | חלי וראובן – חביות בירה · Beer barrels 3 h and 2 h | 6165-6206 | Equal times: you can't add different times, take the common multiple 6 h → 2 + 3 = 5 barrels in 6 h → equal ratios ÷5 → 6/5 h = 1 h 12 min = 72 min | solve-wp26-g096 slides 0-1 (printers 6 h and 10 h → 30 h, 8 batches, 225 min) + wp-094-2 slide 1 (the method itself) | SAME (English adds the rates method, the two-worker shortcut T1·T2/(T1+T2) and the trap "8 is batches, not hours") |
| 3a | שאלות צוות – מבוא · Team questions intro | 6208-6237 | Same, constant rate, "like robots"; considered hard, need understanding (direct/inverse), not technique; how to spot: "identical constant rate" + a group of workers | wp-097 slides 0-1 | SAME (English adds slide 2: team rate = workers × one worker's rate) |
| 3b | 4 נגרים, 20 כיסאות, 3 שעות – יחסים · Carpenters by ratios | 6238-6278 | Team/work/time table; ask what each change does to the time: work ×3 → time ×3; team ×1.5 → time ÷1.5; 9/1.5 → ×2 to drop the decimal → 18/3 = 6 | wp-097 slides 3-4 (cooks 6/30/2 → 4/40/?) and solve-wp26-g098 slide 0 (gardeners) | SAME (her example became English question g098; English writes the flip as a fraction, ×3/2, so the decimal 1.5 never appears) |
| 3c | שיטת ה-V + "צריך עוד זמן" · The V method | 6279-6332 | Same table, order team/work/time (the work must be in the middle); mnemonic + anecdote "צריך עוד זמן"; draw the V over 3 numbers, multiply them, divide by what's left; cancel first (60/20); "in seconds, no thinking, like magic" | wp-097-2 slide 1 + solve-wp26-g098 slide 1 | SAME (mnemonic → "Teamwork takes time"; English also shows the V equals the ratio calculation) |
| 3d | V הפוך · Upside-down V | 6333-6352 | The V must join 3 numbers; when the work is missing, flip the V (6, 20, 6 → 60 = check back with the same example); closing: two ways, understanding (ratios) and the V | wp-097-2 slides 2-4 (cooks: 4, 30, 6 → 60 pies) | SAME (new example instead of reversing her first one; English adds "when to use which", which she gives only in Q105) |
| 4a | זמן עבודה · Work time | 6356-6372 | Time one worker alone would need = time × number of workers (2 workers × 3 h = 6) | wp-099 slides 0-2 (3 workers × 4 h = 12, the boss who pays by the hour; sharing worker-hours) | SAME (her "boss pays salaries" image is used here and in g100) |
| 4b | סלילת כביש · Road: 20 workers 10 days, then 15 workers 10 days | 6375-6400 | The contractor counts paid work-days: 200 + 150 = 350 days for one worker | wp-099 slide 3 (stages, 5×3 + 2×4) + solve-wp26-g100 (fence 14×9 + 6×11 = 192) | SAME (English adds the traps "only the first stage" and "add workers and days first" = 400) |
| 5 | סורקים מהירים/איטיים · 4 fast = twice 6 slow (Q, medium) | 6403-6458 | (1) Equation 4F = 2·6S, "תן למסכן" (double the smaller side, not the bigger) → F = 3S. (2) Plug in numbers: slow = 1 page/min → 6 → 12 → fast 3; "you don't need to know where to start, just roll" | solve-wp26-g101 (5 large = twice 10 small → 4) | SAME (both methods, "give it to the little guy", "we don't need to know where to start"; English adds the trap choice 1) |
| 6 | חפרפרת וגנן · Mole 20 holes/h, gardener 30 per 75 min, 40 holes, 5 h (Q, medium) | 6460-6545 | Ratios ×5 → 100; units: hours → minutes ×60 (5 h = 300 min), keep one unit per column; spot 75 → 300 = ×4 (or ×2 ×2); if not, triangle value 30·300/75 with **her shortcut "when you see 75 and a multiple of 100, reduce by 25"**; 40 + 100 − 120 = 20. Second way: minutes → hours ÷60 (30 → ½, 90 → 1½), 75 min = 1¼ h = 1.25 ("don't confuse 15 and 25"), 1¼ → 5 is ×4 | solve-wp26-g102 (queue +18/h, baker 15 per 40 min, 60 orders, 4 h) | CHANGED: same structure and both unit directions (4 h = 240 min; 40 min = ⅔ h, with the warning "40 minutes isn't 0.4 hours", which replaces her 1.25 warning). With the new numbers **the "reduce by 25" shortcut and the triangle-value fallback are gone** (40 → 240 = ×6 is easy to see). English adds an insight method (net change per 2 h) and the catch-up tool (gap ÷ extra rate) |
| 7 | מכסחות דשא · Mowers 300 m² in 2 h and 50 m² in 3 h, 100 m² in minutes (Q, medium+) | 6547-6645 | (1) Equal times 6 h → 900 + 100 = 1000 in 6 h = 360 min → ÷10 → 36. (2) Estimate: A alone 100 m² in 40 min, so together < 40 (rules out 40, 48); 2 A's would take 20, B helps only a little (elephant and mouse) → a bit less than 40 → 36 | solve-wp26-g103 (polishers 200 m²/4 h and 30 m²/6 h, 110 m²) | SAME (both methods, both bounds, the elephant-and-mouse joke) |
| 8 | אביבה, בתיה וגאולה · Three together 6 h, A+B 12 h, Geula per hour (Q, medium+/hard) | 6647-6724 | Merge A+B into one worker "אביבתיה" (the coffee joke); equal times 12 h: 2 jobs − 1 job → Geula 1 job in 12 h → 1/12. Insight: in 6 h A+B do half, so Geula does the other half → Geula alone = A+B together; two equal workers halve the time | solve-wp26-g104 (Omar, Priya, Sam: 9 h and 18 h → 1/18) | SAME (merge trick, coffee joke, equal times, insight; English adds the subtract-the-rates method and the rule "whenever two workers' time together is given") |
| 9 | שולחן וכיסא · 10 carpenters table 3 h, 9 carpenters chair 5 h, both in 15 h (Q, medium+) | 6726-6854 | (1) V method with two parallel teams → 2 + 3 = 5. (2) Ratios, "easier here": when only one factor changes use ratios, when two change use the V; more time → fewer workers (×5 time → ⅕ workers), "send the rest home". (3) Work time: 30 and 45 worker-hours computed separately (2 and 3 carpenters), then together 75/15 = 5 | solve-wp26-g105 (stage and seating, 8 h → 3 + 7 = 10) | SAME (all three methods, "send the rest home", the trap 26 added. In method 3 English does only the combined 24 + 56 = 80 → 10, not also each job separately; minor) |
| 10 | מגדל המים · Water for 220 dunams for 5 days → 100 dunams (Q, hard) | 6856-6981 | On purpose starts with an estimate: 110 = half of 220 → 10 days; 100 is a bit less than 110 → a bit more than 10 days → **the estimate alone picks 11** (rules out 8 and 10). (2) Plug in numbers: 1 liter per dunam a day → 1,100 L → 11. (3) Team V: dunams (trees) are the workers, drinking water is the work, the tower = 1 → 5·1·220/100 = 11; "the hard part is seeing who is the team" | solve-wp26-g105b (hay for 200 sheep for 9 days → 150 sheep) | CHANGED: all three methods and the "on purpose, estimate first" are kept, but with the new numbers **the estimate no longer finds the answer**: half → 18 days, 150 > 100 → fewer than 18, and "the estimate can't decide" between 12 and 15. Her point was that the half-benchmark lands right next to the answer and decides it. English adds the general rule "the ones who use up a supply are the team" |
| 11 | 20 שאלות תרגול עצמי · 20 self-practice questions (no video) | 6983 | — | wp26-p01 … p20 (book questions 1-20); p10 (circle floor) was moved to topic 33's practice (it needs circle area); plus q-r26-t26-07/-08/-09 and p23-p25 | SAME (all 20 kept, new numbers) |

**Count by row (21 rows): SAME 19 · CHANGED 2 (6, 10) · PARTIAL 0 · MISSING 0.**

### Count by video (her 11 units)

| Unit | Match |
|---|---|
| Lesson 1 מבוא להספק (1a-1e, incl. the Yuval example) | SAME |
| Lesson 2 הספק משותף (2a-2c, incl. pool and beer) | SAME |
| Lesson 3 שאלות צוות (3a-3d) | SAME |
| Lesson 4 זמן עבודה (4a-4b, incl. the road) | SAME |
| Q scanners (101) | SAME |
| Q mole and gardener (102) | CHANGED (the "reduce by 25" shortcut and the triangle-value fallback were lost with the new numbers) |
| Q mowers (103) | SAME |
| Q Aviva/Batya/Geula (104) | SAME |
| Q table and chair (105) | SAME |
| Q water tower (105b) | CHANGED (the estimate no longer decides the answer) |
| 20 practice questions | SAME |

**By video: SAME 9 · CHANGED 2 · PARTIAL 0 · MISSING 0.**

---

## 2. English → Hebrew (English videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| wp-092 slide 3 | Two worked uses of the triangle (pump time, printer rate) | none (her triangle had no numbers) | no |
| wp-092-2 slide 1 | Units in the lesson: ×60 / ÷60, the trap 4 × 2 hours | her unit lesson sits inside Q102 (6475-6531) | no |
| wp-092-3 (whole video) | Two changes multiply the factors (not add); a factor that goes the opposite way is flipped; a percent rate change (25% faster → time ×4/5, not −25%) | none (her team-question ratios are the seed) | no |
| solve-q-r26-t26-01 | 20% faster → 50 min (flip 6/5), plug in a job size | none | no |
| wp-094 slide 2, slides 4-5 | Never add the times; call the job one; fraction rates and "2/15 = 2 pools in 15 h" | slides 4-5 = her pool question (2/9), moved into the lesson | no |
| wp-094-2 slides 2-4 | Choose an easy job size; the range check (less than the faster alone, more than half of it); the two-worker formula T1·T2/(T1+T2) | the range check comes from her Q103 estimate; the rest none | no |
| solve-q-r26-t26-02 | Range check alone picks 6 h; plug in size; the formula | none | no |
| wp-097 slide 2 | Team rate = workers × one worker's rate | none | no |
| wp-099 slide 4 | A worker joins in the middle: what's done + what's left | none | no |
| wp-099-2 (whole video) | Workers join one after another (step table); breaks on a timeline | none | no |
| solve-q-r26-t26-03 | Pipe B joins after 3 h: what's left ÷ combined rate | none | no |
| solve-wp26-g102 slides 2-3 | Insight (net change per 2 h); the catch-up tool (gap ÷ extra rate) | none | no |
| solve-q-r26-t26-04 | Average rate = total work / total time; estimate; the seesaw from topic 25 | none | no |
| r26-t26-factors (whole video) | Compare by factors (multiply every factor, flip the opposite ones); limit: a fixed amount more is not a factor | none (generalises her team ratios) | no |
| solve-q-r26-t26-21 | Budget +20%, price ×1.5 → factors, plug in numbers | none | no |
| Extra methods inside her questions | g093 formula + plug in; g095 plug in size; g096 rates + formula; g104 subtract the rates; traps in every question | none | no |
| r26-t26-summary | Replaced by the summary page (summary_pages/t26.json), not read aloud | none | — |
| practice q-r26-t26-07/-08/-09, wp26-p23-p25 | Extra practice questions | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **Q105b: the estimate decides the answer** (half-benchmark lands next to the answer: 110 → 10 days, 100 a bit less → a bit more than 10 → 11) | solve-wp26-g105b slide 0. Rework the numbers so the half-benchmark lands next to one choice, e.g. hay for 200 sheep for 9 days → **90 sheep**: 100 sheep → 18 days, 90 is a bit fewer → a bit more than 18 → choices 15 / 18 / 20 / 27 → 20 (200·9/90 = 20). The plug-in (1,800 units / 90 = 20) and the V (200·1·9/90 = 20) still work. About 2 sentences change, none added | no | **Restore.** It is the reason she starts this question with the estimate ("on purpose"); now the English says the estimate can't decide, which teaches the opposite of her point |
| 2 | Q102: **"when you see 75 and a multiple of 100, reduce by 25"** (and the triangle-value fallback when the ratio isn't obvious) | solve-wp26-g102 slide 0. Would need her kind of numbers, e.g. the baker completes 30 orders every 75 minutes, 5 hours (300 min): ×4, or 30·300/75 reduced by 25 → 120. The 1¼-hour second way (75 min = 1.25 h, "don't confuse 15 and 25") would come back with it | no | Optional. A good arithmetic habit, but it is a calculation tip, not a work-and-rate method, and the English already keeps both unit directions and an equivalent decimal-hours warning |
| 3 | Q93: "you can also go across the row (y → 2x), either direction gives 6x" | solve-wp26-g093 slide 0, one sentence | no | Not needed; the across-the-row ratio is taught in topic 22 |
| 4 | Q105 method 3: worker-hours for each job separately before combining | solve-wp26-g105 slide 3, one sentence | no | Not needed; the combined count is the same method and shorter |

Nothing is wrong in the English compared with her (all the English answers and traps were rechecked). Nothing in topic 26 is recorded
yet, so both changes are free.
