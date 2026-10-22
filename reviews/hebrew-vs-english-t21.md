# Topic 21 (Trial and error): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/02-Word-Problems-Original-Subtitles.txt`, lines 16-1071 (all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t21.py`), the base
  translation `studio-build/base-v18.html` (window.COURSE, `sourceSegment` fields), and the practice questions (scratchpad dump `ext/course/q21.txt`).
- Recording status from `python3 video_status.py`. **Not recorded:** only `wp-001` (the camera lesson, part 1).
  **Recorded and done:** every other topic-21 video: wp-001-2, wp-003, wp-006, wp-008, wp-012, wp-016, wp-022, all 16 `solve-wp21-g0xx`,
  solve-q-r26-t21-01 and -02. So any restore below means re-recording a recorded video.

**Match scale** (as in the t23 report). The English course gives every question new numbers on purpose, so new numbers alone are not
a change. SAME = same idea and every one of her methods. CHANGED = same idea, but a method, example or structure differs (the cell
says what). PARTIAL = some of her content is missing (the cell says exactly what). MISSING = no English equivalent.

**Her method names in English.** ניסוי וטעייה → "trial and error"; בעיות כלליות → "general problems"; מינימום מקסימום → "minimum and
maximum"; חוקיות → "patterns"; פרה פרה / איבר איבר → "step by step" / "term by term"; סדרות → "a sequence with a formula in n";
דילוג → "the skip"; הצבה מהאמצע → "start from the middle"; פסילה לפי חלוקה → "divides by three / must be even"; ספרה אחרונה →
"the last digit"; הבנה של טווח / טווח רציף → "the ends of the range / no holes"; מקרי קצה → "the edge cases"; קצוות (in patterns) →
"the edges"; מחזור קבוע → "a fixed cycle"; מכנה משותף → "a common multiple" (English uses the correct term; she says "common
denominator").

**The id gaps (wp-002, g011).** The ids follow her subtitle segments. Segment 1 and 2 are her course-flow notes (line 16 "theory",
line 18 "same style: video, question, video…"); English wp-001 is an English-written opening hung on segment 1, and 002 has no video.
Segment 11 is the note on line 238 ("then advanced learning, same style"), also not a video. Nothing was merged or dropped there.
Her sequences intro (lines 194-201, spoken at the end of the eggs video) was moved into the English patterns lesson wp-008.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / every method | English equivalent | Match |
|---|---|---|---|---|---|
| 1 | בעיות כלליות – מבוא · General problems, intro | 20-33 | Trial and error = try, get it wrong, try again (pun: טעות, not תהייה); general problems "depend on luck": nothing tells you what to try first; sometimes the first try works, sometimes several | wp-001 slide 2 (definition, the pens/notebooks example) + wp-003 slide 1 | SAME (the Hebrew pun is untranslatable and was dropped) |
| 2 | חלליות · Spaceships (2 large, ×3 split, 3 hits) | 35-71 | Draw and shoot; first hit must be large; two paths; path 1 gives 5 (luck); path 2 gives 5 or 2 (2 not a choice → try again); "no way to know what to try, and that's fine" | solve-wp21-g004 slides 0-1 (bubbles, ×5 split, 2 large) | SAME (both paths, "lucky on the first try", "try, miss, try again"). English adds an insight (a large pop = +4, a small one = −1) |
| 3 | פקק · Traffic jam (cars 4 m, motorbikes 2.5 m, 1 m gaps; what CANNOT be) | 73-117 | "Cannot" → build what can and cross it out; at least one of each → start car + motorbike; **quick-calc tip: add the halves first, complete the addends to round numbers** (2.5 + 2.5 = 5, 4 + 1 = 5); 9 is skipped (7.5 + any vehicle passes it); checks the other choices too "in case you started from the end"; closing: next lessons let us think and save tries | solve-wp21-g005 slide 0 (truck 10 m, car 4 m, 2 m gaps) + slide 1 (insight: length + 2 divides by 6) | CHANGED: the English numbers are whole, so her "add the halves first" tip has nothing to work on; it is replaced by the base's general grouping tip ("count the vehicle and its gap together", 6 and 12). The skip logic and checking every choice are there. English adds the divisibility insight. Her closing line is covered by wp-001-2 (the three types) |
| 4 | מינימום מקסימום – מבוא · Min and max, intro | 119-128 | Ranges; understanding tells you which way to push, so fewer tries; the motif returns all over the chapter (geometry, overlap problems) | wp-006 slides 1-2 | SAME |
| 5 | קוקיות · 20 hair ties, different amounts, max friends | 130-162 | Bold words on the exam (largest vs smallest); "in theory one friend, or 9 + 11"; to maximise friends give each the minimum: 1, 2, 3, 4, 5 = 15; the 5 left can't make a 6th friend (5 is taken), so spread them among the others → 5 | solve-wp21-g007 slide 0 (42 postcards → 8 friends) | SAME (bold-word tip, "in theory one friend", the running total, the leftovers given to an existing friend). English adds a second method (1 + … + k = k(k+1)/2 by pairing) |
| 6 | חוקיות – מבוא · Patterns, intro | 164-170 | Mostly trial, little error; step-by-step: write the items one by one until you reach what they ask | wp-008 slides 0-1 | SAME |
| 7 | אכילת ביצים · Egg-eating contest (half minus one, 30 → stage 4) + sequences intro | 172-201 | 30 → 14 → 6 → 2, term by term; "you don't need a table on the exam, just 1, 2, 3, 4". Then: sequences are rarer; a general-term or sum formula; don't use school arithmetic/geometric formulas, they don't fit; solving by understanding is rare, plugging in numbers is easiest | solve-wp21-g009 slide 0 (bakery 78 → 8) + wp-008 slide 1 (the sequences intro) | SAME (the "no table" tip, "no school formulas", "understanding is rare, plugging in is safe"). English adds a halve-first order trap and a second method (run the rule backwards from the choice) |
| 8 | אריה בקזינו · Arie doubles his winnings, total through day n | 203-236 | Skip the "understanding"; plug in n = 3: 2 + 4 + 8 = 14; check every choice (only choice 1 gives 14). **Why 3 and not 1: NITE usually builds the choices so that n = 1 leaves two choices; 3 is small enough for an easy calculation and big enough to tell the choices apart** | solve-wp21-g010 slides 0-1 (app downloads, 5 → total 35) | PARTIAL: n = 3, checking every choice and the demonstration that n = 1 leaves two choices are all there. **Missing: her general rule for choosing the number** ("small enough to calculate, big enough to separate the choices") and her remark that the exam builds the choices this way on purpose. English only says "it's small, so the days are easy" and "here, plugging in one leaves two choices… try another easy number" |
| 9 | ניסוי וטעייה מתקדם – מבוא · Advanced trial and error, intro | 240-267 | It looks like luck but there are techniques; why the exam loves these: it predicts first-year university success; school spoon-feeds (the history teacher, the matriculation question bank "these exact questions"); university is self-study; these questions test who freezes and who starts; used all through the chapter | wp-012 slide 1 | SAME (condensed: her school stories become one sentence, "at school we got the material, and often the exact questions too") |
| 10 | מטבע 7/11 · Coin 7 and 11, 5 tosses, which sum CANNOT be (Q, medium) | 269-329 | "Cannot" → cross out 3; work in order from the minimum (all 7s = 35); swap 7 → 11 = +4 each time, so no need to recompute (35, 39, 43, 47, 51, 55); **the skip** (43 → 47 jumps over 45, you can stop there); constant difference; remainder rule: all sums leave 3 when divided by 4, 45 leaves 1 | solve-wp21-g013 (chip 2 and 6, 7 tosses, 32 impossible) | SAME (in order from the minimum, +4 per swap, "the skip" by name, "being inside the range is not enough", the remainder method with a why). English goes straight to the +4 step instead of first computing a sum the long way |
| 11 | ספארי · Lions = 2× zebras, fewer than elephants, 50 animals (Q, medium) | 331-393 | "Could be" because there is a range; just test the choices; **start from the middle** (20 fails and also rules out 22: one plug, two choices); once a choice works on a "could be" question, mark it, there can't be two; **divisibility elimination**: twice a number → even (15 out), three times → divides by 3; "the choices steer you to the convenient plug" | solve-wp21-g014 (choir: sopranos = 3× altos, fewer than tenors, 63) | SAME (from the middle, one plug rules out two, the ×2 → even / ×3 → divides by 3 rule, "24 fits, so we choose it"). English adds a border-case method (tenors = sopranos → 27) and the habit "for 'more than', look at 'exactly equal' first" |
| 12 | אדניות · 20 window boxes, 70 flowers, at least 3 each: which CANNOT be the number with exactly 3 (Q, very hard) | 395-486 | Wordplay ניסוי וטעייה / ותהייה / ובהייה: don't wonder, don't stare, plug in or skip; plug in 10 (4 each), 12 (34 ÷ 8 is more than 4, so it fits: 7 boxes of 4 + 6), 13 → mark 9 without checking; check 9 anyway to understand it (43 ÷ 11 < 4 → one more box stuck at 3); "long = one or two minutes, not twenty; quick questions buy the time"; promise of a shortcut in the next lesson | solve-wp21-g015 (22 baskets, 80 apples → 7) | SAME (don't sit and stare / skip and come back, the "more than four is fine" shortcut, checking the answer for understanding, the time argument, the promise). The Hebrew wordplay is untranslatable |
| 13 | מינימום מקסימום מתקדם – מבוא · Min and max, advanced intro | 488-493 | To make one item as big as possible, give the minimum to the others; deeper nuances through guided practice | wp-016 slides 0-1 (rule 1, 3 different numbers sum 26 → 23; 4 numbers sum 20 → 14) | SAME. English adds two more rules (slides 2-3, see section 2) |
| 14 | מבחן בחשבון · 9-15 questions, a third or more right, 18 students (Q, easy+) | 495-545 | Min: shortest test × ⅓ = 3, × 18 = 54; max: longest test, and "a third **or more**" means all 15 can be right, × 18 = 270; mental calc 18 × 10 = 180, **18 × 5 = half of that, 90**; **last digit**: 3 × 8 → 4 eliminates two choices, 5 × 8 → 0 eliminates the third; saves seconds and silly mistakes | solve-wp21-g017 (10-25 words, a fifth or more, 14 students → 28 and 350) | CHANGED: min and max and the "at least ≠ exactly" trap are the same. With the English choices the last digit only works for the minimum (350 and 140 both end in 0), so English says "here the last digit can't help, it helps only when the choices end in different digits" (a useful added rule; her method is shown fully in g019). Her "× 5 = half of × 10" shortcut is not used (English does 10 × 25 + 4 × 25) |
| 15 | כדים · 7 jars, 8 and 32, each at least 2 more: exact range of jar 4 (Q, easy+) | 547-571 | Min: give the jars before it the minimum (10, 12, 14); max: work back from the last jar with the smallest steps (30, 28, 26); 14-26 | solve-wp21-g018 (8 piggy banks, 5 and 47, +4 → 17-31) | SAME. English adds "the last bank can still hold 47" and a second method (test values from the choices) |
| 16 | גן · 13 children, 5-6 + 3-4 sweets, eat 1-2: total left (Q, medium) | 573-605 | Per child 8-10; fewest left = get least, eat most (6); most = get most, eat least (9); × 13 = 78 and 117; last digit again (6 × 3 → 8, 9 × 3 → 7) | solve-wp21-g019 (fair, 23 children → 46 and 184) | SAME (both methods; English adds the trap "every child uses at least one ticket") |
| 17 | גולות · Adi > Dor > Roni, 21 marbles, all different: Adi's min and max (Q, medium) | 607-680 | (1) Plug in the answers, smartly: for "at least" try the smaller option first (7), for "at most" the bigger (19); 7, 6, 5 = 3 × 6 = 18 < 21 → 8; 19 leaves 1 + 1, not different → 18. (2) Understanding: max = give the others the minimum (1, 2) → 18; min: two people → the bigger is more than half, three → the biggest is more than a third; 7, 7, 7 is equal, so move a marble to Adi from Roni (not Dor, who must stay above Roni) → 8, 7, 6; max is the easy part; "if you lack the understanding, one more plug after the max" | solve-wp21-g020 (Lior > Maya > Noam, 36 cards → 13 and 33) | SAME (both methods, which choice to try first, more than half / more than a third with a why, "the biggest is the easier part"). English does not say *why* the card moves from Noam rather than Maya (she does) |
| 18 | חזרה לאדניות · Back to the window boxes (as promised) | 682-785 | The same question again. **Range is continuous** (every value from min to max works); sort the choices 9, 10, 12, 13: the impossible one must be at an end → 9 or 13, one plug; **edge cases**: all 20 with 3 = 60, too few; 19 → 57 and the last box takes 13 → top is 19, so the problem is at the bottom → 9; "hard, mainly for strong students, watch it again" | solve-wp21-g021 (90 stickers, 26 children → 13) | CHANGED: all her methods are there (the ends of the range, one check; the edge cases 26 fails / 25 works, so the bottom). But it is **a new question of the same type**, not the same question revisited (the base kept her structure: g021 was the same 24-boxes question as g015). English adds a third method (count the spare stickers: at least 26 − 12 = 14) and an important caveat she doesn't give: "no holes" holds only when the value moves by one (the chip's jumps of four left holes) |
| 19 | חוקיות מתקדם – מבוא · Patterns, advanced intro | 787-802 | Recap: patterns, no school formulas, no equation; term by term; now a nuance and psychometric thinking to shorten | wp-022 slide 0 | SAME. English adds cycle tools (slides 1-2, see section 2) |
| 20 | לול · Hen house: doubles, 20 collected, 65 eggs, end of day 3 before collection (Q, medium) | 804-853 | Work neatly, day by day: 65 → 130 → 110 → 220 → 200 → 400; **the edges**: before collecting, so 400 (not 380); always ask what has happened at the start and what happens at the end; inside the sequence nothing goes wrong, the edges are where the trap is | solve-wp21-g023 (bacteria, 40, ×2, −30 → 140) | SAME (every step, "working neatly is the most important thing", the two edge questions, the trap 110 named) |
| 21 | כדורגל · 40 trainees, one ball in every 3 neighbours, Ido 1st has a ball: where can Itamar be (Q, medium) | 855-984 | Every 3 **neighbouring** children (sliding, not blocks); with a ball / without; on the exam a circle and a line; count to 25; "looks long, 10-15 seconds"; shortcut: draw one block (circle, line, line) and count along it; **fixed cycle → remainder**: balls at 1, 4, 7 … leave remainder 1 on ÷ 3; 25 ✓ | solve-wp21-g024 (60 flags, one red in every 5, flag 3 red → 43) | SAME (sliding groups, circle/line, "ten seconds", the one-block shortcut, the remainder method). English counts by fives from 3 instead of counting every item one by one |
| 22 | קפה · Yaron every 12 min, Idit every 15, together at 8:00, third time (Q, hard) | 986-1067 | Write both lists neatly (8:12, 8:24 … / 8:15, 8:30 …), but that is slow; they meet at a common multiple; **jump by the bigger number** (30, 45, 60 → 60 divides by 12), fewer jumps; every 60 min → 8:00, 9:00, 10:00 | solve-wp21-g025 (buses 16 and 20 min, 6:40, fourth time → 10:40) | SAME (listing, then the common multiple by jumping with the bigger gap, with why). English adds the gaps-vs-times count (four times = three gaps, ten posts = nine gaps) and the trap 9:20 |
| 23 | 20 שאלות תרגול עצמי · 20 self-practice questions (no video) | 1070 | — | wp21-p01 … p20 in the practice section, plus p21, p25, p27 and q-r26-t21-06/-07/-10 | SAME (all 20 kept, new numbers) |

**Count by row = by video (her 23 units, including the practice set):** SAME 19 · CHANGED 3 (3, 14, 18) · PARTIAL 1 (8) · MISSING 0.

By her lessons: General problems (1-3) CHANGED (only the halves tip); Min and max (4-5) SAME; Patterns (6-8) PARTIAL (the
choose-n rule); every advanced video SAME except Q14 (CHANGED, last digit only half-works with the new numbers) and Q18 (CHANGED, a
new question instead of the same one revisited).

---

## 2. English → Hebrew (English topic-21 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| wp-001 (whole video, camera) | Opening of word problems: stories hide math (total cut into parts, a ratio, a short list); trial and error shown on pens $3 / notebooks $5 = $19 and $20 | none (her chapter starts straight at general problems) | **no** |
| wp-001-2 slide 1 | The three types with mini examples (5 friends / 20 sweets → 16; doubling and −3 sequences) | only as her lesson titles | yes |
| wp-001-2 slide 2 | Reminder: must / could / cannot (two numbers summing to 14) | none in this topic (from topic 1) | yes |
| wp-001-2 slide 3 | "Try every question on paper before its video" | none (her "video, then a question" format) | yes |
| solve-wp21-g004 slide 2 | Insight: a large pop = +4, a small pop = −1 | none | yes |
| solve-wp21-g005 slide 1 | Insight: length + 2 is made of 12s and 6s, so it divides by 6 | none | yes |
| solve-wp21-g007 slides 1-2 | 1 + 2 + … + k = k(k+1)/2, by pairing the ends | none | yes |
| solve-wp21-g009 slide 0 (part) + slide 1 | The order trap (halve first, then −1); running the rule backwards from a choice | none | yes |
| solve-wp21-g014 slide 1 (part) | The border case (tenors = sopranos → 27) and "for 'more than', look at 'exactly equal' first" | none | yes |
| wp-016 slides 2-3 | Rule 2: make the biggest as small as possible → share equally (26 → 9, 9, 8); rule 3: make one as small as possible → give the others the most (scores ≤ 10); why 2 and 3 aren't opposites | none (she only gives rule 1) | yes |
| solve-wp21-g017 slide 1 (part) | "The last digit helps only when the choices end in different digits" | none | yes |
| solve-wp21-g018 slide 1 | Method 2: test values from the choice ranges | none | yes |
| solve-q-r26-t21-01 (whole video) | Socks in the dark, "to be sure": worst luck + 1; plug in the answers | none | yes |
| solve-wp21-g021 slide 0 + caveat | Method "count the spare stickers"; "no holes only when the value moves by one" | none | yes |
| solve-q-r26-t21-02 (whole video) | "Must be true" with 5 different numbers summing to 20: break each choice, then a min-max proof | none | yes |
| wp-022 slides 1-2 | Cycles: days of the week (remainder ÷ 7), last digits of powers (3²², 2¹⁰), "remainder 0 = the last in the cycle" | none (her remainder idea in Q21 is the seed) | yes |
| solve-wp21-g025 slide 1 (part) | Times vs gaps (4 times = 3 gaps; 10 posts = 9 gaps) | none | yes |
| r26-t21-summary | Replaced by the summary page (summary_pages/t21.json), not read aloud | none | — |
| practice wp21-p21, p25, p27, q-r26-t21-06/-07/-10 | Extra practice questions (not videos) | none | — |

---

## 3. Missing from English: restore?

Every target video below is **already recorded** (status "done"), so any restore means re-recording that video or a patch of it.

| # | Her content | Where it would go | Length | Target recorded? | Recommendation |
|---|---|---|---|---|---|
| 1 | **Choosing the number to plug in a sequence**: "small enough to calculate easily, big enough to tell the choices apart; n = 1 often leaves two choices" | solve-wp21-g010 slide 1, replacing "Here, plugging in one leaves two choices standing" | 1-2 sentences | yes | **Optional** (lean restore at the next re-record). English shows the n = 1 failure by example and says "try another easy number", so the student can still solve; what's lost is her rule for picking the number up front. Drop her claim that the exam builds the choices this way on purpose unless it is checked against real exams first (memory rule *verify before adding*) |
| 2 | Q17: why the marble moves from Roni and not from Dor | solve-wp21-g020 slide 1, after "Let's move one card from Noam to Lior" ("not from Maya, because Maya must stay above Noam") | 1 sentence | yes | Optional; small but it answers the obvious student question |
| 3 | Q18: the shortcut shown on the **same** hard question the student struggled with (her "as promised, we're back to this question") | solve-wp21-g021 would need to reuse the g015 apples question (as the base did) | whole video | yes | Not needed. All her methods are there; a fresh question of the same type is good practice, and English says "the same type as the apple baskets" |
| 4 | Q3: "add the halves first, complete to whole numbers" | solve-wp21-g005 | — | yes | Not needed. The English lengths are whole numbers, and the general idea (group into convenient chunks) is kept as "a vehicle with its gap" |
| 5 | Q14: "× 5 = half of × 10" (18 × 5 = 90) | solve-wp21-g017 slide 0 (14 × 25 could be shown as "half of 14 × 50"… not natural) | 1 sentence | yes | Not needed; a mental-math aside, and English uses a clean split instead |
| 6 | The Hebrew wordplay (טעות / תהייה / בהייה) | — | — | — | Not needed; untranslatable, and its point ("don't sit and stare") is kept in g015 |

**Nothing to RESTORE outright.** No English part is wrong compared with her; in two places English is more careful than the Hebrew:
she says the min-max range is always continuous (English g021 adds that it holds only when the value moves by one, citing the chip
question), and she calls the meeting time a "common denominator" (English: "common multiple").
