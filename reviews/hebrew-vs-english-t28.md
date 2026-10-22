# Topic 28 (Counting possibilities / צירופים): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/02-Word-Problems-Original-Subtitles.txt`, lines 8289-9793 (all of it read).
- English: topic 28 has no reading scripts yet (only `ai_scripts/r26-t28-summary.json`), so the English side is the per-topic dump
  `scratchpad/ext/course/t28.txt` (every video's spoken text) and `q28.txt` (the 54 questions), plus `base-v18.html` /
  `Psychometric-Teacher-Studio-v19-hybrid.html` for on-screen text and the base lessons.
- **Recording status:** none of the topic-28 ids (wp-123 … solve-wp28-g144, r26-t28-*) appears in any `video_status.py` list
  (record / reread / send / done / check). The tracker does not cover this topic, so nothing here is recorded; every
  restore below goes into a not-yet-made video, and the topic is about to be rewritten anyway.

**Match scale** (as in the t23 report). New numbers alone are not a change. SAME = same idea and all her methods. CHANGED =
same idea, but a method, example type or order differs. PARTIAL = some of her content is missing (the cell says what). MISSING =
no English equivalent.

**Video numbering.** There are no gaps: her subtitle segments 123-144 map one-to-one onto the English ids. 123 = lesson 1
intro, 124 = the trial-and-error example, then **wp-124-after** = the rest of lesson 1 (the product rule), 125 / 126 = its two
examples; 127 = lesson 2, 128-130 its examples; 131 = lesson 3, 132-133; 134 = lesson 4, 135-136; 137 = lesson 5, 138-139;
140-144 = the five advanced questions. **wp-140-after** and **wp-141-after** are the "extensions" she gives *inside* her
questions 140 and 141, split off into their own short lessons. In the English course her worked lesson examples became
try-first questions with solution videos, and the lesson videos became short intros (memory rule *teach-in-question-videos*).
The base translation still had full lessons (e.g. base wp-124-after had "Why we multiply" and "Order doesn't matter"
slides); that teaching now lives in solve-wp28-g125.

**Her names → English.** ניסוי וטעייה → "trial and error / listing"; מכפלת אפשרויות → "multiplying the possibilities";
שלב בחירה → "stage of choice"; בחירה תלויה → "one choice depends on another" (wp-141-after: "Forced digits"); עם / בלי
החזרה → "with or without repetition", "the pool"; עצרת → "factorial"; פעולה הדדית → "mutual action"; סדרה יורדת / עולה →
"each time one fewer" (g133) / "one plus two plus three…" (g143); חיבור / חיסור אפשרויות → "adding / subtracting
possibilities"; סידורים פנימיים → "internal arrangements"; בחירה משלימה, n−1 מתוך n → "complementary choice", "n minus one
out of n", "who stays out"; מאורע משלים → "the complementary event".

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | מבוא לצירופים · Intro: what combinatorics is | 8290-8301 | "Combinatorics" comes from "combination" = possibilities; we count ways to arrange or choose, by the question's data; type 1 = trial and error, just count | wp-123 slides 0, 3 | SAME (English adds slide 1 "what counts as a different result" and slide 2 "at most / at least → Topic 21 method") |
| 1b | ניסוי וטעייה – ספרות 1-4 עולות · Trial and error: increasing digits from 1-4 (item 124) | 8303-8333 | Just check: 123, 124, 134, 234 → 4; "we counted, we checked" | solve-wp28-g124 slide 1 (digits 3, 5, 6, 9) | SAME (English adds the tip "list smallest first" in wp-123 and Method 2: choose the one digit left out → 4) |
| 1c | מכפלת אפשרויות – בר-סלט · Product rule: salad bar 3 × 5 (item 125) | 8323-8392 | Most exam questions aren't listed but use a technique; options at every stage of choice, then multiply; write the options per stage; **why multiply** (5+5+5 = 3×5); **order of the stages doesn't matter** (drink first: 3+3+3+3+3 = 5×3) | wp-124-after (2 short slides) + solve-wp28-g125 (7 soups × 3 breads) | SAME (all three points are in g125: "why multiply", the grid "soup first or bread first, the order doesn't matter"; English adds the trap "adding counts menu items") |
| 1d | בחירה תלויה – מספר עובד, סכום 10 · Dependent choice: employee number, digit sum 10 (item 126) | 8393-8469 | First digit can't be 0 (0 needs 10, "10 is a number, not a digit") → 9; second digit is forced → 1; 9 × 1 = 9; the common mistake 9 × 9; "imagine you picked, then ask what completes it" | solve-wp28-g126 slide 1 (sum 14 → 5 × 1) | SAME (the "14 is a number, not a digit" reason, the dependency and the 5 × 5 mistake are all there; English adds a listing check, 59 ≠ 95, 77 counted once) |
| 1e | סיכום שיעור 1 · Lesson-1 recap | 8458-8469 | Two kinds: trial and error, or multiply the options per stage | none in t28 (the idea is in r26-t28-summary: "Work in stages… a short list with no pattern? Just list") | SAME (moved to the topic summary) |
| 2a | עם או בלי החזרה – מבוא · With or without repetition: the pool | 8471-8478 | Choosing from a pool (digits 0-9 or a restricted set); check whether the item picked left the pool or can be picked again | wp-127 slides 0-1 (the question is on screen: "Did the item leave the pool — or can I pick it again?") | SAME |
| 2b | 1-5, עם החזרה · Three-digit numbers from 1-5, repeats allowed (item 128) | 8480-8504 | 5 × 5 × 5 = 125; "the 3 goes back into the pool" | solve-wp28-g128 (lock 1-9, 9³ = 729) | SAME (adds "444 / 777 counts"; base wp-127 slide 3 "a three-digit number does not mean different digits") |
| 2c | 1-5, ספרות שונות · Three-digit numbers from 1-5, different digits (item 129) | 8506-8540 | 5 × 4 × 3 = 60; the pool shrinks; with vs without compared ("if I picked again, only 2 options") | solve-wp28-g129 (9 × 8 × 7 = 504) | SAME (adds "don't divide: 123 and 213 are different codes") |
| 2d | סידור איברים בשורה – 5 ספרים · Items in a row: 5 books (item 130) | 8541-8626 | A row = choosing without repetition; 5·4·3·2·1 = 120; the ! sign = factorial (5!, 4!, 100!); n items in a row = n!; factorial will be used in later formulas; recap: with = pool full, without = pool shrinks, a row is the special case of without | solve-wp28-g130 (7 trophies, 7! = 5040) | SAME (definition, n!, "we'll use it again later" are kept; her "a row is the special case of without repetition" is implicit: "that trophy is placed — it's out") |
| 3a | פעולה הדדית – קווי תעופה · Mutual action: flight lines between 4 countries (item 132) | 8629-8752 | Mutual action = between two items at once, common on the exam; 4 × 3 = 12 is not among the choices; she lists all 12 lines to show each is counted twice (Washington–Russia and back); "with 10 countries you won't draw" → compute as usual (10 × 9) and divide by 2 → 6; examples: handshakes, paths between houses, games between teams, polygon diagonals | wp-131 + solve-wp28-g132 (6 towns, 30 / 2 = 15) | SAME (English adds the roles caveat (president/secretary → don't halve) and a listing check 5+4+3+2+1, which is her "descending series" from 3b. In English the doubled 30 is a trap choice, not "missing from the choices") |
| 3b | אלכסונים במשושה · Diagonals of a hexagon, 4 ways (item 133) | 8753-8814 | Rare but appears. (1) Draw and count (9); "they won't give a 20-sided polygon". (2) Mutual action 6 × 5 / 2 = 15 lines, minus 6 sides. (3) Descending series 5+4+3+2+1 = 15, minus 6. (4) Formula n(n−3)/2 | solve-wp28-g133 (octagon → 20, the same 4 ways) | SAME (English adds the trap 40 = forgetting to halve) |
| 4a | חיבור או חיסור אפשרויות – מבוא · Adding or subtracting cases: intro | 8816-8834 | Can't count in one go → split into cases; very rare (once every few years), considered very hard; usually 2 cases, count each and add | wp-134 slides 0-2 | SAME (English adds "cases must not overlap", the case-heading tip, and "probability uses it") |
| 4b | רביד – קולה ← אגוזי · Ravid: cola forces a nut bar (item 135) | 8836-8897 | Case 1 cola → 1 × 1 = 1; case 2 not cola → 3 × 5 = 15 (the nut bar included); 16 | solve-wp28-g135 (espresso → croissant: 1 + 25 = 26) | SAME (English adds "the rule works one way only" and Method 2: 30 − 4 forbidden) |
| 4c | חיסור אפשרויות – שתי קוביות, סכום ≠ 4 · Subtracting: two fair dice, sum not 4 (item 136) | 8865-8953 | Even rarer; a rule forbids some arrangement → all minus forbidden; "fair dice" explained (not weighted); 36 − 3 (1-3, 2-2, 3-1) = 33; adding the allowed cases is possible but messier; recap: rare, near the end of the section | wp-134 slides 3-4 + solve-wp28-g136 (sum ≠ 8: 36 − 5 = 31) | SAME (English adds "colors matter, 4-4 counted once", a direct check, and the cue words "not / at least one". The "fair dice" explanation is not in topic 28 (the English stem has no "fair"); it is taught in topic 29 wp-146, where "fair" first appears) |
| 5a | בחירה ללא חשיבות לסדר – בחירת קבוצה · Choosing a group (order doesn't matter): intro | 8955-8986 | Until now order mattered (a row); edge questions, very hard and very rare; choosing 4 of 10 children, Danny-then-Yossi = Yossi-then-Danny → doubling; "a rule full of words sounds like Chinese, let's see an example" | wp-137 slides 0-2 | SAME (English uses 3 of 9; "Six different picking orders — one and the same group") |
| 5b | גן – 6 ילדים לשתי קבוצות של 3 · Kindergarten: 6 children into two groups of 3 with different teachers (item 138) | 8988-9094 | 6 × 5 × 4 as usual; she shows the same 3 children picked in 6 different orders = one group; internal arrangements = 3! (lining the 3 up); 6·5·4 / 3! = 20; "regular calculation, divide by the factorial of the number chosen" | wp-137 slide 2 ("Divide by k!") + solve-wp28-g138 (10 hikers, 5 to Lena and 5 to Omar: 10·9·8·7·6 / 5! = 252) | SAME (English adds step-by-step cancelling, "the second group is decided", and Method 2: don't halve, the guides have names) |
| 5c | בחירה משלימה – 5 מתוך 6 · Complementary choice: 5 of 6 children (item 139) | 9095-9216 | n−1 of n = n; why: choose the one left aside (she goes through the 6 children one by one); also by the group method 6·5·4·3·2 / 5! = 6; recap: the group type is very rare, the complementary type more common and simple | wp-137 slide 3 ("Who stays out", 14 of 15) + solve-wp28-g139 (11 of 12, both methods) | SAME (English extends it: 8 of 10 = choose the 2 left out, "always count the smaller side") |
| 6 | לימוד מתקדם · Advanced section header | 9218 | Only a header, no spoken intro | solve-wp28-g140 opens "The first advanced counting question" | SAME |
| 7a | 6! / 4! (Q, easy+) · Rows of 6 over rows of 4 (item 140) | 9219-9271 | (1) n items in a row = n!; write out and cancel → 6 × 5 = 30. (2) Shortcut: 6! = 6 × 5!, = 6 × 5 × 4!, cancel 4! | solve-wp28-g140 (9!/7! = 72) | SAME (both methods) |
| 7b | הרחבה: n! · (n+1)! · Extension: factorial algebra (inside item 140) | 9272-9301 | Pure factorial expressions; (1) psychometric way: plug in a number (3! · 4!); (2) the math: (n+1)! = (n+1)·n!, so n!·(n+1)! = (n!)²(n+1) | wp-140-after slides 1-3 (n!·(n+2)! with n = 2; = (n!)²(n+2)(n+1)) | SAME (n+2 instead of her n+1, the same two methods. English adds slides 4-7: "a product of factorials is not one factorial", 120/720/5040 by sight, a run of neighbours (b!/a! = 56), factorials and primes) |
| 8a | תלת-ספרתי, מאות + אחדות = 5 (Q, medium) · Hundreds + units = 5 (item 141) | 9303-9332, 9392-9410 | She starts with the **tens digit, because it is free** (10); hundreds 1-5, not 0 ("there's no number 076"); units forced → 1; 5 × 10 × 1 = 50; tip: write the number of options above each position and list them below | solve-wp28-g141 slide 1 (sum 8 → 8 × 10 × 1 = 80) | CHANGED: English starts with the **most restricted** position (hundreds) and does the free tens digit last; her order (free digit first) is not used. Everything else is kept (the "above/below" tip, "no such number as 058", the dependency). English adds a listing check and the trap 90 |
| 8b | הרחבה: כל הספרות זהות / אחדות = מאות · Extension: all digits identical (9) / units = hundreds (90) (inside item 141) | 9333-9391 | 111, 222…: 9 × 1 × 1 = 9, not 9 × 9 × 9; units = hundreds: 9 × 10 × 1 = 90 (101, 111, 121…); "choosing the hundreds digit really chooses two digits" | wp-141-after (five-digit: all identical = 9, not 9⁵; "mirror" digits 9 × 10 × 10 × 1 × 1 = 900) | CHANGED: same idea and same sentences, but (a) five-digit examples instead of her three-digit ones and (b) moved from *before* the answer (she pauses mid-solution to teach it, then returns) to a separate lesson *after* the question. Nothing missing |
| 9 | ריבוע ABCD – B זוגי, C·D לא אי-זוגי (Q, hard) · Digits 1-4 in a square (item 142) | 9412-9526 | (1) B even: 2 options; product odd only if both odd → **easier conclusion: A must be odd** (2), then 2 and 1 → 8; nuance: a square, not a row, doesn't matter — multiply per stage. (2) Trial and error, organised: anchor 2 and 1, change as little as possible; 4 options with 2 in the corner → by symmetry 4 more with 4 → 8 | solve-wp28-g142 (2, 5, 6, 9; A even, C×D even → B odd) | SAME (both methods, the "easier conclusion", the square nuance, the anchor and the symmetry. English adds Method 3: 12 − 4) |
| 10 | טורניר כדורסל – 28 משחקים (Q, medium+) · Tournament with 28 games (item 143) | 9528-9706 | (1) Mutual action n(n−1)/2 = 28 → n(n−1) = 56 = product of consecutive numbers 8 × 7 → 8. (2) Plug in the answers (10 → 45 ✗, 8 → 28 ✓); aside: start from the middle (5 → 10, too few, so 4 is out too), not needed with such easy arithmetic. (3) Ascending series: a table, each new team adds one game per team already there, 1+2+…+7 = 28; warning: **8 teams, not 7**; write it across the page; "whatever you prefer" | solve-wp28-g143 (66 matches → 12 players) | SAME (all three methods, the middle-start aside, "twelve, not eleven", "across the page") |
| 11 | 6 סטודנטים, 5 בסדר גובה יורד (Q, medium+/hard) · 5 of 6 students by height (item 144) | 9708-9790 | (1) Trial and error with heights 1-6, change only the right end; 6 rows; sanity check: 5 is fewer than found, 5! = 120 far too many. (2) Insight, the complementary event: choose who stays ("you stay, everyone else come") → 6; "the complementary event isn't magic, it's a technique worth knowing" | solve-wp28-g144 (7 of 8 children → 8) | SAME (both methods, the sanity check and her closing line) |
| 12 | 20 שאלות תרגול עצמי · 20 self-practice questions (no video) | 9792 | — | wp28-p01 … p20 in the practice set, plus p23, p24, p26 and q-r26-t28-14/-16/-19/-21/-29/-31/-41 | SAME (20 kept, with new numbers) |

**Count by row (25 rows):** SAME 23 · CHANGED 2 (8a, 8b) · PARTIAL 0 · MISSING 0.

### Count by video (her 23 units)

| Unit | Match |
|---|---|
| Lesson 1 intro + trial-and-error example (1a, 1b) | SAME |
| Product rule + salad bar (1c) | SAME |
| Dependent choice, employee number (1d, 1e) | SAME |
| Lesson 2 with/without repetition (2a) | SAME |
| Example 125 (2b) | SAME |
| Example 60 (2c) | SAME |
| Books in a row, factorial (2d) | SAME |
| Lesson 3 mutual action, flights (3a) | SAME |
| Hexagon diagonals (3b) | SAME |
| Lesson 4 add/subtract (4a) | SAME |
| Ravid (4b) | SAME |
| Dice sum ≠ 4 (4c) | SAME |
| Lesson 5 choosing a group (5a) | SAME |
| Kindergarten (5b) | SAME |
| 5 of 6 (5c) | SAME |
| Advanced header (6) | SAME |
| Q 6!/4! (7a) | SAME |
| Extension n!(n+1)! (7b) | SAME |
| Q hundreds + units = 5 (8a) | CHANGED (order of positions) |
| Extension identical / mirror digits (8b) | CHANGED (5-digit examples, moved after the question) |
| Q square (9) | SAME |
| Q tournament (10) | SAME |
| Q students by height (11) | SAME |
| 20 practice questions (12) | SAME |

**By video: SAME 22 · CHANGED 2 · PARTIAL 0 · MISSING 0** (24 units including the practice set).

This is the most faithful topic so far: every named method, shortcut, warning and closing line of hers is present, and every
one still works with the English numbers (checked: 5 × 1, 9³, 9·8·7, 7!, 30/2, octagon 20 four ways, 1 + 25, 36 − 5,
252, 12, 9!/7!, n!(n+2)! at n = 2 → 48, 8 × 10 × 1, 8, 12 players, 8 rows).

---

## 2. English → Hebrew (English topic-28 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? |
|---|---|---|
| wp-123 slide 1 | "Decide what counts as a different result" (row vs committee vs code) | none |
| wp-123 slide 2 | "At most / at least / must be true" questions are Topic 21 extreme questions, not counting | none |
| solve-wp28-g124 slide 2 | Insight: choose the one digit left out | none (it is her complementary idea from 5c / 11, used early) |
| solve-wp28-g132 (part) | Roles (president/secretary) → don't halve | none |
| wp-134 slides 2-3 (parts) | Cases must not overlap; case headings; "not" / "at least one" → all minus forbidden; count both the same way | none |
| solve-wp28-g135 slide 2, g136 slide 2, g142 slide 3 | Extra check methods (complement / direct count) | none |
| wp-137 slides 3-4 | "Count the smaller side" (8 of 10 = 2 of 10 = 45); the 5-step checklist (on the memory card) | none |
| solve-wp28-g138 slide 2 | Labelled groups → don't halve (unlabelled → 126) | none (her example had labelled groups but she didn't raise it) |
| wp-140-after slides 4-7 | Product of factorials ≠ one factorial; 120 / 720 / 5040 by sight; a run of neighbours (b!/a! = 56 → a = 6, b = 8); factorials and primes | none |
| r26-t28-cases (whole video) + solve-q-r26-t28-04, -05 | Test a formula on a small case; choices differ by a factor (210 vs 35); "at least once" = all minus none; objects into boxes (3⁵) | none |
| r26-t28-arrange (whole video) + solve-q-r26-t28-06, -07, -08, -09 | Together → glue; apart → gaps or all minus together; repeated letters (BANANA); round table (n−1)! | none |
| solve-q-r26-t28-28 | (10! − 9!)/8!: take out the smaller factorial | none |
| r26-t28-summary | Spoken topic summary | none (her section ends straight in the practice set) |
| practice wp28-p23, p24, p26, q-r26-t28-14/-16/-19/-21/-29/-31/-41 | Extra practice questions | none |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | Q141: her order "start with the free tens digit" | solve-wp28-g141 slide 1 | no | **Not needed.** English deliberately teaches "most restricted position first" (the wp-137 checklist and the summary); starting with the free digit gives the same product, and two contradictory orders in one topic would confuse. Optional half-sentence: "The tens digit is free, so we can write its ten options at any point" |
| 2 | Q141 extension with her three-digit examples (111…999 = 9; units = hundreds = 90), taught *inside* the question before the answer | wp-141-after | no | **Not needed.** The five-digit versions teach the same thing and are a step harder; teaching it after the question matches the English "video, then question" flow. For the rewrite: keep the line "choosing the first digit really chooses two digits at once" (it is her sentence) |
| 3 | "Fair dice" = not weighted, every face equally likely (her aside in item 136) | — | — | **Not needed in topic 28**: the English g136 stem doesn't say "fair", and topic 29 wp-146 teaches the word where it first matters |

**RESTORE list: empty.** Nothing of hers is missing.

### Notes for the writers of the rewrite (checklist)
Keep, per video, these points of hers (all present now; don't lose them in the rewrite):
- g124: "we counted, we checked". g125: why multiply (3 for each of 7) + stage order doesn't matter. g126: "14 is a number, not a
  digit", the forced second digit, the 5 × 5 mistake, "imagine you picked, then ask what completes it".
- wp-127 / g128-g130: did the item leave the pool; pool full vs shrinking; factorial definition and n!; "we'll use factorial again".
- g132: count as usual, then divide by 2, because A→B = B→A; her list of cues (handshakes, paths, games, diagonals).
- g133: all four ways (draw, mutual action − sides, descending series − sides, n(n−3)/2).
- wp-134: rare, very hard, near the end of the section. g135: split into two cases, add. g136: all minus forbidden, and listing the
  allowed cases directly is possible but messier.
- wp-137 / g138: the same group picked in different orders, divide by k! = the internal arrangements. g139: choose who stays out,
  and the group formula cancels to n. "The complementary type is more common and easy."
- g140: both ways (write out, or stop at 7!). wp-140-after: plug in a number first, then the math.
- g141: "write the options above, list them below"; no leading zero. wp-141-after: "the forced position gets one".
- g142: "the easier conclusion: B must be odd"; square vs row doesn't matter; anchor + symmetry.
- g143: consecutive numbers 12 × 11; plug in the answers + the "start from the middle" aside; ascending series and "twelve, not eleven".
- g144: organised listing + sanity check against the other choices; the complementary event, "not magic, a technique".

### Anything wrong in the English?
Nothing wrong found; all English answers check out. Two small notes:
- wp-127 slide 1 says "after every pick, ask one question" without saying the question; the question is only on screen ("Did the
  item leave the pool — or can I pick it again?"). If the narration is re-voiced, say the question aloud too.
- wp-124-after, wp-127 and wp-131 are now 2-slide intros (the base had full lessons); that is intended (teach in question videos),
  and their teaching is all in g125 / g128-g130 / g132.
