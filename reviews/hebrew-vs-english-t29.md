# Topic 29 (Probability): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/02-Word-Problems-Original-Subtitles.txt`, lines 9794-11057 (all of it read).
- English: the per-topic dump `scratchpad/ext/course/t29.txt` (every video's spoken text) and `q29.txt` (44 questions);
  `studio-build/base-v18.html` only to check the practice ids.
- **Recording status:** no topic-29 video is in `video_status.py` at all (not in record / reread / send / done / check), because
  topic 29 has no reading scripts yet. So **nothing in topic 29 is recorded**; every fix below can go straight into the rewrite.

**Match scale.** New numbers on their own do not count as a change (memory rule *questions-differ-from-hebrew*).
SAME = same idea and every one of her methods, new numbers only. CHANGED = same idea, but the method, the example type or the order
is different. PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Her names → English.** רצוי חלקי מצוי → "wanted over possible"; "always the מצוי first" → "Possible first"; הסתברות משלימה →
"the complementary probability / the complement"; קשר של וגם / או → "And → multiply", "Or → add"; היסטוריה → "History: does the
past change the future?"; בחירה ראשונה לא משנה → "First pick / first spinner doesn't matter"; **בחירה תלויה → "a forced choice"**
(see row 2d: topic 28 in English says "depends on the first", not "forced"); סימטריה בקוביות → "Dice symmetry", "Distance from 7";
חוק ינטה → "the law of Jante"; הצבת מספרים → "plugging in numbers"; הברקה → "insight / a small psychometric flash".

**Id numbering (no gaps).** wp-146 lesson 1 → g147-g150 her lesson-1 examples, with **wp-147-after** = her black-balls example
(9860-9871) cut out as a tiny lesson right after g147, in her order. wp-151 lesson 2 → g152-g158 her lesson-2 examples. wp-159
lesson 3 (dice symmetry) → g160. g161-g165 = her five advanced questions. Then the English-only r26 block.
Practice ids p03, p21, p24, p26, p27 existed in the base and were removed (p24's "1-30 divisible by 4 or 6" now sits in
solve-q-r26-t29-01 slide 2; p26's "music students" became the wp-146 example); none of them is hers.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | מבוא להסתברות · Intro: wanted over possible | 9795-9828 | Continues combinatorics; "high chance" is not a measure, math gives a number; probability = רצוי/מצוי, always a fraction; between 0 and 1 (all good → 1, none → 0, never 1.5 or 2⅓); **tip: always write the מצוי first, then the רצוי** | wp-146 slides 1-4 | SAME (English adds "count equally likely outcomes" and "possible = the group they choose FROM", 18 music students of 40) |
| 1b | קובייה הוגנת – מספר זוגי · Fair die, even number | 9830-9858 | "Fair die" = an ordinary one, NITE always writes it so nobody says "I have other dice"; possible first: 6; wanted 2,4,6 → 3/6 = 1/2; "too easy for the exam, it's just to learn the routine" | solve-wp29-g147 (spinner 1-10) + the "fair" note in wp-146 slide 2 | SAME (the die became a 10-section spinner, so the "fair die" note moved to wp-146; English adds method 2, pairing odd/even) |
| 1c | כד עם כדורים שחורים בלבד · Only black balls, chance of white | 9860-9871 | No white balls → wanted 0, possible "some x, doesn't matter" → 0 | wp-147-after | SAME (English adds the other edge: all good → 1, "certain", and "an answer above 1 or below 0 means a mistake") |
| 1d | 4 אדומים ו-3 כחולים · 4 red, 3 blue | 9874-9895 | Possible 7, wanted 4 → 4/7; **common mistake: "we draw one ball, so wanted = 1"**; picture all 7 balls, each red one is good | solve-wp29-g148 (7 green, 4 yellow) | SAME |
| 1e | ירדן הוציא 2 כחולים · Yarden already took out 2 blue | 9898-9914 | Possible = 7 left (not 9); wanted 5 − 2 = 3; "it already happened, it's the past, it doesn't interest us" → 3/7 | solve-wp29-g149 (11 orange, 7 white, 4 orange out) | SAME (English adds "don't multiply by the chance of those first draws" and method 2, equal groups) |
| 1f | הסתברות משלימה · Complementary probability | 9915-9929 | All probabilities add to 1: pass 2/3 → fail 1/3; coin 1/2 + 1/2 | solve-wp29-g150 slide 1 (pass 3/4 → fail 1/4; coin) | SAME (taught inside the question video that uses it, right before the example, as in her order) |
| 1g | 15 כדורים, שחור 2/5 · 15 balls, black 2/5, how many white | 9932-9954 | Complement: white 3/5; x/15 = 3/5 → cross-multiply → x = 9 | solve-wp29-g150 (36 tokens, red 4/9 → 20 blue) | SAME (English adds method 2: find red first, then the trap "16 is the red count") |
| 1h | סיכום שיעור 1 · Lesson-1 recap | 9955-9964 | Wanted/possible, possible first, complement to 1; "not a complex topic on the exam" | r26-t29-summary (summary page) + wp-146 slide 1 ("a pretty simple topic") | SAME |
| 2a | הסתברות של מספר מאורעות · Several events: and / or | 9966-9982 | Two connections: "and" → multiply, "or" → add; "or" is very rare and harder | wp-151 | SAME (English adds: add only cases that can't happen together, a 2 or a 5 on a die = 1/3, and a pointer to the overlap question) |
| 2b | קובייה ומטבע · Coin and die: heads and 3 | 9984-10006 | And → ½ × 1/6 = 1/12 | solve-wp29-g152 (coin + 5-spinner, 1/10) | SAME (English adds a counting check, 10 pairs) |
| 2c | 3 הטלות מטבע · Coin 3 times, all heads | 10009-10023 | ½ each, and-and-and → 1/8 | solve-wp29-g153 (5 tosses, 1/32) | SAME (+ counting check) |
| 2d | סכום 6 בשתי קוביות · Two dice, sum 6 | 10026-10082 | List the pairs (5 of 36, "you could stop here") but practise each die separately: first die anything but 6 → 5/6; second die **only one good result, because it depends on the first ("remember dependent choice from combinatorics"; "rewind, or go back to the combinatorics dependent-choice questions")** → 5/6 × 1/6 = 5/36 | solve-wp29-g154 (sum 5: 4/6 × 1/6 = 1/9) | PARTIAL: both methods are there and the numbers work (a 5 or 6 is too big). **Missing: her link to combinatorics** — English calls it "a forced choice" and never says it is the dependent choice from topic 28 (topic 28 in English says "depends on the first"). English adds the 36-cell grid and the 1/18 trap |
| 2e | היסטוריה – יורם וארבל · History: Yoram and Arbel | 10083-10137 | The past doesn't affect the future; the coin doesn't know; casino roulette (bet black after 5 reds); a newcomer can't have a different chance → equal; rare on the exam | solve-wp29-g155 (Omar/Kate, 7 in a row) | SAME |
| 2f | דאבל בשתי קוביות + טיפ · Doubles, and the tip | 10139-10192 | First die doesn't matter (6/6), second must match (1/6, "dependent choice again — we saw it in combinatorics, in the last question, and now"); could count 6/36 directly, but **tip: work out each event separately, counting it all at once leads to mistakes** | solve-wp29-g156 (two 5-spinners, 1/5) | SAME (the tip is method 2's last line; the combinatorics link is again only "a forced choice again", see 2d) |
| 2g | עם או בלי החזרה – 3 אדומים 3 צהובים · Without replacement, different colours | 10193-10227 | Recall with/without replacement from combinatorics; draw one after the other even if two come out; first ball doesn't matter (6/6), second: 5 left, 3 of the other colour → 3/5 | solve-wp29-g157 (6 green, 6 white → 6/11) | SAME (English adds method 2, two orders added) |
| 2h | אורי ו-5 דלתות · Uri, 5 doors, opens 2 ("or") | 10232-10296 | Her ONLY method: two cases — right on the first (1/5) OR wrong on the first and right on the second (4/5 × 1/4 = 1/5) → add → 2/5; the common mistake "right on the first or right on the second" (you can't be right on the second without first failing); driving-test image; "hard, rare; rewind if needed" | solve-wp29-g158 (8 boxes, 2 opened → 1/4) | CHANGED: her two-case method is now **method 2**; English opens with a direct count (2 good boxes of 8) and adds method 3 (complement). Her mistake becomes the concrete trap choice 1/8 + 1/7; the driving test is kept. "Hard and rare" is said only in wp-151, not here |
| 2i | סיכום שיעור 2 · Lesson-2 recap + teaser for symmetry | 10297-10309 | And/or, replacement, first choice doesn't matter, second depends on the first | r26-t29-summary | SAME |
| 3a | סימטריה בקוביות · Dice symmetry | 10311-10427 | Sums 2-12; red and blue dice so 1-2 and 2-1 are different; sum 4: don't flip 2-2 (count it once; same for 3-3 in sum 6); counts 1…6…1; opposite faces add to 7; symmetric around 7 | wp-159 | SAME (English adds the proof x → 7 − x and the generalisation: cards 1 to n → top sum n + 1) |
| 3b | A סכום 10, B סכום 4 · A = P(sum 10), B = P(sum 4) | 10429-10463 | Sometimes a story (Yossi bets 7, Dani 9); 10 and 4 are both 3 from 7 → equal; no counting, so no 2-2 confusion | solve-wp29-g160 (8 vs 6) | SAME (story variant kept; English adds a counting proof) |
| 4 | לימוד מתקדם · Advanced section heading | 10465 | A heading only | solve-wp29-g161 opening ("Advanced probability.") | SAME |
| 5 | רותי וצביקה · Ruti and Tzvika, same letter (22 letters, 5 in his name) | 10466-10575 | (1) Calculation: Ruti 5/22, then Tzvika must pick HER letter, 1/5 (not all 5 are good) → 1/22. (2) Insight: order doesn't matter, let Tzvika go first: all his letters are good (5/5 = 1), Ruti must match: 1/22 — "when one choice is all good, put it aside and look straight at the second" | solve-wp29-g161 (Ella 7 days, Omar 2 weekend days → 1/7) | SAME (both methods and the closing rule "when one stage can't go wrong, skip it"; English adds the trap 2/7) |
| 6 | פקולטה למשפטים · a classes, b students, tallest from each | 10577-10713 | (1) 1/b per class, and → (1/b)^a; not in the choices → power of a fraction: 1^a / b^a = 1/b^a. (2) Plug in numbers: 1,1 useless (all choices 1); 2,2 useless (three choices 1/4); **rule: plug into the choices FIRST and make sure they differ — you'd have to plug into them anyway, so reverse the order**; 2 classes, 3 students → 1/9 | solve-wp29-g162 (m rounds, n envelopes → n^−m) | SAME (every step, both failed tries and the rule with its reason; English adds the negative exponent) |
| 7 | עוגיות חמאה · Two bakeries, not-butter cookie | 10715-10789 | (1) One big basket: possible 1200; wanted 950 + 130 = 1080 → 9/10. (2) Complement: butter 120/1200 = 1/10 → 9/10; "like the complementary percent" | solve-wp29-g163 (eggs, 900, not cracked 11/12) | SAME (the basket image and the percent link kept; English adds the trap 1/12) |
| 8 | דניאל והקינוחים · Danielle's desserts (4 kinds, no repeat) | 10791-10884 | Sunday is given → probability 1, don't compute it; Monday: 3 options but only 2 good (not the cake) → 2/3; Tuesday: ice cream back in the pool, 1/3 → 2/9; the key is the dependence between neighbouring days | solve-wp29-g164 (6 classes: 4/5 × 1/5 = 4/25) | SAME |
| 9 | ארנון והסוכריות · Arnon, 4 red + 1 blue, 4th is blue | 10886-11052 | (1) 4/5·3/4·2/3·1/2, "before you calculate, see how it cancels" → 1/5. (2) Symmetry with the Danish "law of Jante" (a long aside): first is 1/5, last is 1/5, 4th is 1/5 — "everyone's equal"; a hard question solved in seconds; three players, who wins round 3 | solve-wp29-g165 (8 tickets, 6th is the prize → 1/8) | SAME (both methods; the Jante aside is shortened to one line, its point kept) |
| 10 | 20 שאלות תרגול עצמי · 20 self-practice questions (no video) | 11054 | — | wp29-p01 … p25 (22 kept; p03, p21, p24 dropped from the base's 27) + q-r26-t29-08, -10 | SAME (as far as can be checked; her 20 questions are not in the subtitles) |

**Count by row (26 rows):** SAME 24 · CHANGED 1 (2h) · PARTIAL 1 (2d) · MISSING 0.

### Count by video (her 22 units)

| Unit | Match |
|---|---|
| Lesson 1 intro (1a) | SAME |
| L1 examples: die (1b), black balls (1c), 4 red 3 blue (1d), Yarden (1e), complement + 15 balls (1f-1h) | SAME ×5 |
| Lesson 2 intro (2a) | SAME |
| L2 examples: coin + die (2b), 3 coins (2c), sum 6 (2d), history (2e), doubles + tip (2f), without replacement (2g), Uri's doors (2h, + recap 2i) | SAME 5 · PARTIAL 1 (2d) · CHANGED 1 (2h) |
| Lesson 3 symmetry (3a) and its question (3b) | SAME ×2 |
| Advanced Qs: letters, classes, cookies, desserts, candies (4-9) | SAME ×5 |
| 20 practice questions | SAME |

**By video: SAME 20 · CHANGED 1 · PARTIAL 1 · MISSING 0.**

---

## 2. English → Hebrew (English topic-29 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| wp-146 slides 2, 4 (part) | "Count outcomes that are equally likely"; "possible = the group they choose FROM" (18 music students of 40) | none | no |
| wp-147-after (part) | Probability 1 = certain; an answer outside 0-1 = a mistake | only implicit in her 0-1 rule | no |
| wp-151 (part) | Add only cases that can't happen together (2 or 5 → 1/3); overlap is counted twice | none | no |
| wp-159 (part) | Proof of the symmetry (x → 7 − x); cards 1 to n → most likely sum n + 1 | none | no |
| Extra methods / traps in g147, g149, g150, g152, g153, g154, g157, g158 (methods 1 and 3), g160, g161, g162, g163 | Check-by-counting, two orders added, direct count, complement, named trap choices, negative exponent | none (her questions had 1-2 methods) | no |
| r26-t29-more-rules (whole video) | "Exactly one": add the orders; find one order × number of orders (3/8) | none | no |
| solve-q-r26-t29-01 | OR with overlap: add, subtract the overlap; Venn diagram; 1-30 divisible by 4 or 6 | none | no |
| solve-q-r26-t29-02 | At least one = 1 − none; traps 27/64 and ¼+¼+¼ | none | no |
| solve-q-r26-t29-03 | Two stages → a tree; don't pour boxes of different sizes together | none | no |
| r26-t29-summary | Summary page, incl. the "three doors" (count / path / symmetry) | her lesson recaps, much expanded | — |
| practice wp29-p22, p23, p25, q-r26-t29-08, -10 (and others beyond her 20) | Extra practice | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **The second die/spinner is a dependent choice, as in combinatorics** (she says it three times: 10055, 10069, 10152-10161) | solve-wp29-g154 slide 2, one sentence where "a forced choice" is said: "It's the dependent choice from counting: the second stage depends on the first." Then g156 can say "a dependent choice again". Use topic 28's English word ("depends on"), or rename both to the same term | no | **Restore.** 1-2 sentences; it ties probability to topic 28, which is how she builds the topic, and "forced choice" is otherwise a new name the student never met in topic 28 |
| 2 | Uri's doors as THE "or" example: her two-case method first; "a hard, rare type — replay it if you need" | solve-wp29-g158: swap methods 1 and 2 (or keep the order and open method 1 with "first the simple way, then the OR way, which you need for harder ones") | no | Optional. Her method and her common mistake are fully there; only the lead changed. Swapping keeps the video the showcase of wp-151's "or" rule |
| 3 | The long law-of-Jante aside (Denmark, the writer, Israeli mentality) | g165 slide 2 | no | Not needed; the one-line version keeps the point |
| 4 | Lesson recaps and the teaser for the symmetry lesson | — | — | Not needed; the summary page covers them |

**Nothing wrong found in the English** (all numbers checked: g154 1/9, g157 6/11, g158 1/4 by all three methods, g162 choices with
m = 3, n = 2, g164 4/25, g165 1/8). One small wording point for the writers: wp-146 slide 4's example ("Forty students, eighteen
of them study music. A music student is chosen. The bottom is eighteen") gives no "wanted", so it reads unfinished; the summary's
choir version (15 of 32) is clearer.

Nothing of topic 29 is recorded, so every item above can go into the rewrite with no re-recording.
