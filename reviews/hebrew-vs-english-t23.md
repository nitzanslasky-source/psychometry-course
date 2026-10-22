# Topic 23 (Percentages): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/02-Word-Problems-Original-Subtitles.txt`, lines 2684-4328 (all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t23.py`), the base
  translation `studio-build/base-v18.html`, and the practice questions in `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`.
- Recording status comes from `python3 video_status.py --list record` (unrecorded) and `--list send` (recorded).
  **Recorded:** wp-052-2, wp-052-3, wp-052-4, wp-053. **Not recorded yet:** wp-052 (part 1), wp-053-2/-3/-4, every topic-23
  solution video, r26-t23-traps.

**Match scale.** The English course gives every question new numbers on purpose (memory rule *questions-differ-from-hebrew*), so new
numbers on their own do not count as a change.
SAME = same idea and every one of her methods, new numbers only. CHANGED = same idea, but the method, the example type or the order
is different (the cell says what). PARTIAL = some of her content or one of her methods is missing (the cell says exactly what).
MISSING = no English equivalent.

**Her name "משוואת האחוז".** English uses the same name, "**the percent equation**" (wp-052-3 slide 1: "The first is the percent
equation", and the wp-052-4 recap). Her other method names also carry over: טבלת אחוזים / יחסים זהים / ערך משולש → "equal
ratios, the ratio table", "the triangle value"; שיטת 10% → "ten percent"; הצבת 100 → "plug in a hundred"; עץ אחוזים → "a percent
tree"; אחוז משלים → "what stays / what's left" (English never uses the word "complement"); הצבת תשובות → "plug in the answers".

**Items 55 and 56 (the jump from g054 to g057).** Neither was a question. Her subtitle segments run 52 = lesson 1, 53 = lesson 2,
54 = the survey question, **55 = the percent-tree video** (3322-3402, which solves the same survey again), **56 = the short
"advanced learning" intro** (3404-3413), 57-65 = the nine advanced questions. In the base translation, **55 was merged into g054**
(it became "Method 2 · Percent tree", and it is still there in the current script, g054 slide 2). **56 was dropped**: its one
idea became the base g057's opening line ("Advanced percentages —"), and the current scripts no longer have even that line.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | חישוב אחוזים – מה זה אחוז · What a percent is | 2685-2714 | A percent is a part of something, like a fraction; 100% = the whole; 1% = one hundredth; 50% = half, 10% = a tenth, 25% = a quarter | wp-052 slide 1 | SAME (English adds "a percent alone is not an amount: 29% of 200 tickets") |
| 1b | מעבר מאחוז לשבר ומשבר לאחוז · Percent ↔ fraction | 2715-2769 | The % sign is a fraction sign; percent → over 100 and reduce (50, 30, 20, 82%); fraction → expand to denominator 100 (3/4 → 75%, 2/5 → 40%) | wp-052 slides 2-3 | SAME (English adds why expanding keeps the fraction equal) |
| 1c | שברים שחשוב להכיר בעל פה · Fractions to know by heart | 2770-2853 | 1/2, 1/4, 1/8 by halving + their decimals; 1/10, 1/5, 1/20; 1/3, 1/6 ("half of 32 is 16, so 16 and a bit"); 12.5 and 12½ written both ways; families 3/8, 5/8, 2/5, 3/5, 4/5, 3/4, 7/20, 9/20 | wp-052-2 slides 1-4 (+ the mem-percent card) | SAME (of the families, English has 3/8, 5/8, 3/5, 4/5 and 7/20; 2/5, 3/4 and 9/20 are not built in this video) |
| 1d | משוואת האחוז · The percent equation | 2854-2938 | Words → equation: "of" = times, % = /100. (1) 60% of 120 = 72, reduce before multiplying. (2) A% of 20 = 35: ×100 → 20A = 3500 → A = 175. (3) (10+x)% of 80 = (60−x)% of 60: ×100, keep the brackets, divide by 20, x = 20. "The hard part is building the equation; the rest is algebra" | wp-052-3 slides 1-3 (45% of 80; x% of 75 = 21; (5+x)% of 60 = (70−x)% of 40) | CHANGED: in example 2 English finds x through the fraction table (75/100 = 3/4, so 3/4 of x = 21) and does not multiply by 100. Her "×100 to clear the denominator" step still appears in example 3 |
| 1e | יחסים זהים / ערך משולש · Equal ratios / the triangle value (percent table) | 2939-3005 | Percent table: 24% of 125 → diagonal ÷ what's left = 30. Then 14% of a number is 56, what is 35%? → triangle value straight away (35×56/14 = 140): "you don't need to find the whole" | wp-052-3 slide 4 (45% of 80 again, by the triangle value) + wp-052-4 slide 1 (15% = 54 → 25% = 90) | CHANGED: (a) the first example reuses the equation's numbers, to compare the two methods, instead of a fresh 24%-of-125 type; (b) the "no need for the whole" example uses a ratio step (÷3 to 5%, then ×5) instead of her diagonal multiplication. The idea "never find the whole" is kept |
| 1f | שיטת 10% · The 10% method | 3006-3080 | 10% = divide by 10 (70, 350; 66 → 6.6, 572 → 57.2: move the decimal point); decimals are rare on the exam; 40% of 70 = 4×7; 35% of 60 = 30% + 5% (half of 10%) and the short way to write it; closing: 10% for mental math, the table when the numbers aren't round, the equation if stuck | wp-052-4 slides 2-3, 5 (240, 48 → 4.8; 30% and 35% of 240; recap) | SAME (English adds slide 4: 30% = 63, so 10% = 21 and the whole is 210) |
| 2a | חישוב אחוז מאחוז – הצבת 100 (פסנתר) · Percent of a percent – plug in 100 (piano) | 3082-3164 | Two types of percent question; whole not given → don't use x, plug in 100; piano +20% then −30% of the NEW price (70% of 120 by 10% = 84) → 16% lower; "the number you get is the answer in percent" | wp-053 slides 0, 3 (+80% then −25% → +35%) | SAME (new numbers; it ends in a rise instead of a drop). English adds, before it, the change rule (slides 1-2) |
| 2b | דמבו הפיל · Dumbo (two drops) | 3165-3188 | 100 kg, −40% → 60, −20% of the new weight (10% = 6) → 48 → lost 52% | wp-053 slide 4 (wood −30%, −20%) | SAME (English adds the "what stays" shortcut, which leads into multipliers) |
| 2c | קובי / יפעת / לאון – מי השלם · Who is the 100? | 3189-3264 | "After the מ comes the whole"; several מ's: the one in the QUESTION decides → Leon = 100, Yifat 120, Kobi = 60% of 120 (or compute 40% and subtract) = 72 → 28% lower | wp-053-3 slides 3-4 (Ben/Tal/Eli) | SAME ("of" / "than" stands in for the Hebrew מ; English computes 55% directly and does not show "or compute 40% and subtract"). English adds the arrow map (slides 5-6) |
| 2d | סקר מעשנים · Survey question (smokers) – Hebrew item 54 | 3265-3321 | Plug in 100 into the survey: 60 non-smokers, 40 smoke, 30% of 40 = 12 filter → 28 without filter, two ways (40−12, or 70% of 40); write the numbers on the question itself | solve-wp23-g054 slides 0-1 (musical instruments) | SAME (both ways: subtract, or 20% = a fifth of 65; the "write on the question" habit is kept). In her course this was a worked example inside the lesson; English makes it a try-first question |
| 2e | עץ אחוזים · The percent tree – Hebrew item 55 | 3322-3402 | The same survey as a tree; each branch becomes the new 100%; common mistake (10% instead of 70%; "50% wouldn't fit"); multiply along the path: 70% of 40% = 7×4 = 28%, because 10% of 40% is 4%; her verdict: more visual but much more writing, plug in 100 is easier | solve-wp23-g054 slide 2 | PARTIAL: everything is there (the new 100%, the common mistake with "80% wouldn't fit", multiply along the path) **except her closing comparison** ("visual, but much more writing; once you practise, plugging in 100 is easier"). The base translation had it; the current script cut it, probably because of the R35 "no which-way-is-better verdict" rule |
| 3 | לימוד מתקדם – פתיח · Advanced percentages intro – Hebrew item 56 | 3404-3413 | 4 sentences: we've learned the basics, now more advanced exam questions "with a few interesting nuances" | none (the base had one line at the start of g057; the current scripts don't) | MISSING (trivial, no teaching content) |
| 4 | צוללן – 82.5% חמצן · Diver, 82.5% of the oxygen used (Q, medium+) | 3415-3509 | (1) 100 − 82.5 = 17.5% left → 17.5/100 → ×2 → 35/200 → 7/40. (2) The choices are built on purpose: 1/20 = 5% (expand to 100) → 7/20 = 35% → 7/40 = half = 17.5%; or 1/40 = 2.5% → ×7 | solve-wp23-g057 (cartridge, 57.5% used → 17/40) | CHANGED: same two methods. In method 2 English starts at 17/20 (= 85%) instead of first converting the simplest choice 1/20, and drops her other path (1/40 = 2.5%, ×7); English adds the trap choice (23/40 = the part used). **Order:** English now puts this question after the stock question (g058 comes before g057 in the flow) |
| 5 | מניית סייברארק · Stock falls 85% (Q, easy) | 3511-3575 | (1) 10% method: 85% of 820 = 8×82 + 41 = 697, then 820 − 697 = 123. (2) Complement: 15% stays = 82 + 41 = 123: "the complementary percent is often easier" | solve-wp23-g058 (coat 680, −75%) | SAME (both methods; English adds the trap that the drop itself, 510, is one of the choices) |
| 6 | 40→44→48 שני ורותם · Price 40→44→48, Shani vs Rotem (Q, medium) | 3577-3630 | (1) 4/40 = 1/10 = 10%; 4/44 = 1/11 < 1/10 (the cake shared by 10 vs 11 children). (2) 10% of 44 = 4.4 → 48.4 > 48, so less than 10%. "Same amount of money, a different percent, because the whole grew" | solve-wp23-g059 (40→50→60) | SAME (both methods, the cake image kept; English names the change rule from wp-053) |
| 7 | דלילה ושמשון · Delilah and Samson, give 30%, get back 40% (Q, medium) | 3632-3797 | (1) Algebra with x: a percent can't stand alone (not x − 30/100); complement 70%·x; then +40% of what's left; the 140% shortcut (and the common-factor algebra) → 98% → 2% fewer. (2) Plug in 100 (whole after the מ) → 70 → +28 → 98. Then 200 → 196 → 4/200 = 2%. Two reasons for choosing 100 | solve-wp23-g060 (Noa's coins) | SAME (every step is there; English writes 70% and 140% as the multipliers 0.7 and 1.4 and adds the trap 40 − 30 = 10%. It doesn't restate "the whole comes after of" here, only "into the whole, the coins she had at the start") |
| 8 | מאיה / אסף / יהונתן · Maya, Asaf, Yehonatan: +25% then −20% (Q, medium) | 3799-3890 | (1) Plug in 100 into Asaf → 125 → −20% (10% = 12.5) → 100 → ratio 1. (2) Insight, consecutive unit fractions: +1/2 −1/3, +1/3 −1/4, +1/4 −1/5 bring you back to the whole | solve-wp23-g061 (+50% then −33⅓%) | CHANGED: the pair is 1/2, 1/3 instead of her 1/4, 1/5, and the insight's examples are +1/6 −1/7, +1/5 −1/6, +1/2 −1/3, with the general rule +1/n −1/(n+1). English adds a 3rd method (the arrow map) and the trap 7/6 |
| 9 | 25% מ-50% של x · 25% of 50% of x = 6, find 37.5% of x (Q, easy+) | 3892-4007 | (1) Algebra: 1/4·1/2·x = 6 → x = 48; **37.5% = 3/8 from the fraction table** → 3/8 of 48 = 18. (2) Swap trick: a% of b = b% of a (73% of 84 = 84% of 73) → 50% of 25% = 12.5% → 12.5% of x = 6; 37.5% = 3×12.5% (or 1/8 → 3/8) → 18 | solve-wp23-g062 (25% of 18% of y = 9, find 13.5%) | CHANGED: both methods are there, but with the new numbers **the fraction-table step is gone** (13.5% is not a table fraction, so English uses 10% + 3% + ½% of 200). Her reminder "review the fraction tables" is lost here. English also adds a second swap example (4% of 75) |
| 10 | לא שווה ל-20% מ-2x · Which is NOT equal to 20% of 2x (Q, medium) | 4009-4146 | (1) Leave everything over 100, so only the numerators need comparing (40x); then "most students just look at the numerator". (2) Inverse relation: double the whole → halve the percent for the same result (20% of 100 = 10% of 200); she checks each choice this way | solve-wp23-g063 (16% of 5y) | SAME (both methods; in English the odd choice out is "double the percent, same whole", in hers both were doubled) |
| 11 | דודי והתפוזים · Dudi's oranges, 85% Sunday, difference 14 (Q, medium) | 4148-4228 | 85 − 15 = 70% ↔ 14; (1) triangle value 15×14/70 = 3. (2) Shortcuts when the ratio isn't obvious: **(a) drop a zero: 70 → 7, 14 is ×2, so 15 → 1.5 → ×2 = 3**; (b) a middle step: ÷7 → 10% = 2 → ×1.5 = 3 | solve-wp23-g064 (70% market, difference 48 kg) | PARTIAL: the triangle value and shortcut (b), the 10% middle step, are there. **Shortcut (a), "divide both by ten to see the ratio", is missing** (in English it appears only as a reduction inside the triangle calculation, not as a way to spot the ratio). English adds the trap "48 is the difference" |
| 12 | בריכה מתאדה 30% בשעה · Pool loses 30% an hour, 98 m³ now (Q, medium+) | 4230-4326 | (1) Plug in 100 — but **as 100%**, because a real amount is given; complement: 70% of 70% = 49% ↔ 98 → ×2 → 200. (2) Plug in the answers: start with the round one (200), 140 → 98 ✓; NITE often makes the round answer the right one | solve-wp23-g065 (barrel, −10% a day, 243 L) | SAME (both methods, the "100%, not 100 liters" warning, and "try the roundest choice first"; English adds the trap 270 = only one day back) |
| 13 | 20 שאלות תרגול עצמי · 20 self-practice questions (no video) | 4328 | — | wp23-p01 … p20 (book questions 1-20) in the practice section, plus p24-p26 and q-r26-t23-09/-11/-12 | SAME (all 20 kept, with new numbers) |

**Count by row (22 rows):** SAME 14 · CHANGED 5 (1d, 1e, 4, 8, 9) · PARTIAL 2 (2e, 11) · MISSING 1 (3).

### Count by video (her 14 units)

| Unit | Match |
|---|---|
| Lesson 1 חישוב אחוזים (1a-1f) | CHANGED (only the equation and triangle-value examples were reworked; nothing is missing) |
| Lesson 2 חישוב אחוז מאחוז (2a-2c) | SAME |
| Survey question (2d), item 54 | SAME |
| Percent tree (2e), item 55 | PARTIAL (her closing comparison with plugging in 100 was cut) |
| Advanced intro, item 56 | MISSING (trivial) |
| Q diver (57) | CHANGED |
| Q stock (58) | SAME |
| Q 40→44→48 (59) | SAME |
| Q Delilah/Samson (60) | SAME |
| Q Maya/Asaf (61) | CHANGED |
| Q 25% of 50% (62) | CHANGED (the fraction-table step was lost) |
| Q not equal to 20% of 2x (63) | SAME |
| Q Dudi's oranges (64) | PARTIAL (the "drop a zero" ratio shortcut is missing) |
| Q pool (65) | SAME |
| 20 practice questions | SAME |

**By video: SAME 8 · CHANGED 4 · PARTIAL 2 · MISSING 1** (15 units including the practice set).

---

## 2. English → Hebrew (English topic-23 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| wp-052 slide 1 (part) | "A percent alone is not an amount" (29% of 100 vs 200 tickets) | none (her idea, from g060: "a percent can't stand alone") | no |
| wp-052-4 slide 4 (part) | 10% when the whole is missing (30% = 63 → 210) | none in her lesson (the base's "More tools") | yes |
| wp-053 slides 1-2 (part) | The change rule: change ÷ original × 100; up 25% vs down 20% for the same 5 credits; the trap of dividing by the new price | only implicit in her Q59 | yes |
| wp-053 slide 5 (part) | When plugging in 100 fails (a fixed amount is added) | none | yes |
| wp-053-2 (whole video) | Multipliers (×0.7, ×1.4), chains multiply, +20% −20% = −4%, the rule that +p% then −p% loses p²/100 % | none (her 140% shortcut in Q60 is the seed) | no |
| wp-053-3 slides 1-2 | Working backwards (−20% → 96, so the price was 120; the pond: ×0.8 ×0.5) | only inside her Q65 | no |
| wp-053-3 slides 5-6 | The arrow map; "x is 25% more than y → y is 80% of x" | none | no |
| wp-053-4 (whole video) | Same part with two wholes → flip the percents (Dan/Gil); same whole → keep them; recap | none (her Q63 inverse relation is related) | no |
| solve-wp23-g061 slide 2 | 3rd method, the arrow map | none | no |
| solve-q-r26-t23-01 | +25% then −12%: multipliers, plug in 100, the formula p + q + pq/100 | none | no |
| solve-q-r26-t23-16 | 45% of the novels = 30% of the textbooks, 600 books: the flip rule + plug in the answers | none | no |
| r26-t23-traps | Estimating a percent (90 out of 320) with benchmark percents, then the intro to 3 trap questions | none | no |
| solve-q-r26-t23-03 | "150% of" vs "150% more than": plug in 100 + the arrow map | none | no |
| solve-q-r26-t23-04 | A mixture (add sugar from 20% to 40%): what stays the same + plug in the answers | none | no |
| solve-q-r26-t23-05 | Letters (N, g): plug in numbers + the algebra | none | no |
| r26-t23-summary | Replaced by the summary page (summary_pages/t23.json), not read aloud | none | — |
| practice wp23-p24, p25, p26, q-r26-t23-09, -11, -12 | Extra practice questions (not videos) | none | — |

Removed from the base, not added: the base wp-052 "More tools" slide (the swap trick, the missing whole, the change rule) was
spread out. The swap is now only in g062 (where she teaches it), the missing whole is in wp-052-4, and the change rule is in wp-053.

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **Q64 shortcut (a): "drop a zero to see the ratio"** (70% ↔ 14: 7 → 14 is ×2, so 15 → 1.5 → 3) | solve-wp23-g064 slide 2, before the 10% middle step. With the English numbers: 40% ↔ 48 → "4 → 48 is ×12, so 3 → 36" | no | **Restore.** It is one of her two named shortcuts and costs about 2 sentences |
| 2 | **Q62: 37.5% = 3/8 from the fraction table** ("review the tables you must know by heart") | solve-wp23-g062. The 13.5% target isn't a table fraction, so it would need new numbers whose target is a table fraction (e.g. ask for 37.5% or 62.5% of y) | no | **Restore if the numbers are reworked** anyway; this is the only place in the topic that practises the fraction table inside a question |
| 3 | Percent tree: her closing comparison ("more visual, but more writing; once you practise, plugging in 100 is faster") | end of solve-wp23-g054 slide 2 | no | Optional. It is a "which way is better" verdict, which R35 bans; a neutral version ("the tree is more visual; plugging in a hundred needs less writing") would keep her point without a verdict |
| 4 | Q57: start by converting the simplest choice (1/20 = 5%), and her other path 1/40 = 2.5% → ×7 | solve-wp23-g057 slide 1 | no | Optional, minor; English already teaches "the choices are built on purpose" |
| 5 | The advanced-section intro (item 56) | one line at the start of solve-wp23-g058 (now the first advanced question) | no | Not needed; it has no teaching content |
| 6 | The flow order: diver before stock (her 57 before 58) | flow order g057 ↔ g058 | — | Not needed; the English order (the easier stock question first) is deliberate |

Nothing in the recorded parts (wp-052-2/-3/-4, wp-053) is missing any of her content, so no re-recording is needed.
Every restore candidate goes into an unrecorded solution video.
