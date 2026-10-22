# Topic 24 (Overlapping groups): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/02-Word-Problems-Original-Subtitles.txt`, lines 4330-5174 (all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t24.py`), the base
  translation `studio-build/base-v18.html` (videos wp-067/068/069 = her source segments 67/68/69), and the practice list
  `scratchpad/ext/course/q24.txt`.
- Recording status from `python3 video_status.py --list record` / `--list send`: **every topic-24 video is unrecorded**
  (wp-067, -2, -3, wp-068, -2, -3, wp-069, all eight solve-wp24 videos, the three solve-q-r26-t24 videos, r26-t24-two-way,
  r26-t24-three-groups). None is in the "send" (recorded) list.

**Match scale** (same as the t23 report). English questions use new numbers on purpose, so new numbers alone are not a change.
SAME = same idea and every one of her methods. CHANGED = same idea, but a method or step is different (the cell says what).
PARTIAL = some of her content is missing. MISSING = no English equivalent.

**Her names carry over.** גם וגם → "both", רק א' → "music only / art only", לא ולא → "neither", שיטת הריבועים → "the squares
method" (one long rectangle cut into four boxes, filled "like a sudoku"), חפיפה מקסימלית = גודל הקבוצה הקטנה → "the biggest
overlap is the smaller group", חפיפה מינימלית = חריגת סכום הקבוצות מהשלם → "the smallest overlap is the sum minus the total /
how far do the groups go over the total", לכל היותר / לכל הפחות → "at most / at least" (her mnemonic יותר = מקסימום,
פחות = מינימום becomes "at most has the word most… at least has the word least").

**The numbering (g070-g078, no g073).** Her segments: 67 = intro, 68 = the ranges lesson, 69 = the exact-overlap lesson,
70-72 = the three worked examples that follow the exact lesson (fish, marina, economics students), **73 = the heading
"לימוד מתקדם" (line 4712), which has no spoken text at all in her subtitles**, 74-78 = the five advanced questions. So the gap
at 073 is a title card with nothing to translate. English made her 70-72 lesson examples into try-first questions, as in
topic 23.

**Flow order.** English plays the five advanced questions in a different order: g078 (owls → movies) and g077 (lunch →
conference) come right after g072, before g074 (wedding) and g075 (farm class); g076 (company) comes after the new
q-r26-t24-01. So all the exact questions come first and the range questions after them. Hers: 74 wedding, 75 farm, 76 company,
77 lunch, 78 owls.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | בעיות חפיפה – מבוא · Intro: what overlap is (marina) | 4331-4356 | Groups with shared members; marina, sail and motor boats as two circles; "both", sail only, motor only, neither = 4 sub-groups | wp-067 slides 0-2 (class: music/sport; second example: red/electric cars) | SAME (new story; English adds a second picture, the cars, and "every member is in exactly one region") |
| 1b | שני סוגי בעיות + פיצה · Two kinds + the pizza | 4357-4389 | Two kinds on the exam: min/max (range) and exact; pizza, mushrooms on 5 slices, tomatoes on 4: whatever you do at least 1 slice has both, at most 4; "a topping can't go on a slice twice" | wp-067-2 slides 1-2 (6 slices, mushrooms 4, olives 3 → 1 to 3; "we can't put olives on the same slice twice") | SAME (English adds slide 3, the exact version on the same pizza) |
| 2a | תחומי חפיפה – טווחים · Range lesson: definition + kids, hats, horses | 4391-4428 | A fact is missing → only a range; max possible / min that must be; 8 kids, 5 hats, 4 horses, handed out one by one: horses first to kids with no hat → 1 forced; all horses to hat kids → 4 | wp-068 slides 1-2 (15 students, art 10, drama 9, boxes → 4 to 9) | SAME |
| 2b | הטכניקה · Max = smaller group, min = sum − total | 4429-4457 | Max = the smaller group (put the small group inside the big one, nothing to calculate); min = sum of the groups − total, explained as 9 items for 8 kids → 1 item too many must go to a kid who already has one | wp-068 slides 3-4 (+ 20 students dog/cat, 30 players caps/gloves) | SAME (the same "places left over" explanation) |
| 2c | מקרים מיוחדים · Equal groups; groups that don't pass the total | 4458-4475 | 5 and 5 → max 5; 5 + 2 = 7 < 8 → min 0, "not −1: I don't do 7 − 8, I ask by how much they go over the total" | wp-068 slides 3, 5 (6 and 6; 8 + 12 = 20 exactly; 5 + 12 = 17 → "not minus three") | SAME (English adds the "sum exactly equals the total" case) |
| 2d | איך מזהים · Spotting a range question | 4476-4494 | לכל היותר / לכל הפחות / הגדול ביותר / הקטן ביותר / מה יכול להיות; choices like "between 3 and 9", "at least 3, at most 8"; mnemonic יותר = max, פחות = min; "the minimum that must be" | wp-068-2 slide 1 | SAME (mnemonic re-made for English: "most → maximum, least → minimum") |
| 2e | דוגמה: גן ילדים · Example: kindergarten, 20 kids, 15 hats, 12 glasses | 4495-4513 | "What could be" → range; max 12 (smaller group); min two ways: formula 27 − 20 = 7, or logic (5 kids without a hat get glasses first, 7 left must go to hat kids); "most students prefer the formula; very strong students just see it; work how you like" | wp-068-2 slide 2 (24 players, caps 18, gloves 14 → 8 to 14, both ways) | SAME (her "most students prefer the formula" preference line is not said, as the R35 no-verdict rule requires; English says "Both ways give eight") |
| 3a | חפיפה מדויקת – הגדרה + ילדים · Exact lesson: definition + kids with one "neither" | 4515-4569 | All the facts are given → exact sizes; they can ask both / neither / only one group; the same 8 kids, 5 hats, 4 horses + "exactly one kid has neither" → the other kid without a hat must get a horse → exactly 2 both; "the difference from last lesson is this one fact" | wp-069 slides 0-1 (the same 15 art/drama students + "exactly two take neither" → 6) | SAME (English also shows it on the pizza, wp-067-2 slide 3) |
| 3b | שיטת הריבועים · The squares method | 4570-4603 | One long rectangle cut into 4 boxes = the two circles drawn differently; brackets for each group sharing the middle box; all 4 boxes = total; fill "like a domino, a sudoku": neither 1 + horse bracket 4 = 5 → hat only 3 → both 2; "I didn't really need to draw it" | wp-069 slides 2-3 | SAME (her warning that the brackets must share a box, which she gives in the fish example, is here in slide 2) |
| 3c | דגים בבריכה · Fish: 32 fish, 21 floats, 15 snorkel, 12 both → neither (her item 70) | 4605-4642 | Squares method; **common mistake: snorkel bracket must overlap the floats bracket**; snorkel only 15 − 12 = 3; "go left, toward neither"; float bracket 21 + 3 = 24; 32 − 24 = 8; "float only, 9, I could find but don't need" | solve-wp24-g070 (52 guests, pool 31, gym 26, both 17 → 12) | SAME (every step: gym only, "we move to the left", bracket + only = 40, "we could also find pool only, 14, but we don't need it"; the overlap warning was moved into wp-069. English adds a 2nd way, counting each once, and the traps 14 and 5) |
| 3d | מרינה · Marina: 15 boats, 10 motor, 8 sail, 2 neither → both (her item 71) | 4644-4669 | Squares: neither 2 + sail bracket 8 = 10 → motor only 5 → both 10 − 5 = 5 | solve-wp24-g071 (27 printers, color 16, posters 13, neither 3 → 5) | SAME (same chain; English adds a 2nd way, 27 − 3 = 24 in a group, 29 − 24 = 5, and the trap 2) |
| 3e | סטודנטים מתוסכלים · Economics: frustrated econ students = 1/5 of econ, 1/3 of frustrated; ratio (her item 72) | 4671-4710 | Long wording → just two groups; overlap = x ("I could simply plug in 1, but let's take x"); econ 5x, frustrated 3x; only-parts 4x and 2x → twice; "a very hard question on the real exam, but in the boxes it's simple" | solve-wp24-g072 (chess 1/9, robotics 1/4 → 8 : 3) | SAME (x method; her aside "plug in 1" became a full 2nd method, plug in 2; "questions like this scare a lot of students, but in the boxes it's simple" kept. English adds a 3rd way, the flip rule, and the trap 9 : 4) |
| 4 | לימוד מתקדם · Advanced heading (her item 73) | 4712 | A heading only; no spoken text | none (no g073) | MISSING (trivial: nothing to translate) |
| 5 | חתונה · Wedding: 160 guests, 25% bride, 85% groom, at least both (Q, easy) (her item 74) | 4714-4851 | (1) Numbers: 25% = a quarter = 40; 85% by the **complement 15%** (10% + 5% = 24) → 136; "write the data in order"; max = smaller group 40, free; min = 176 − 160 = 16. (2) **Stay in percent**: 110% → 10% too many → 10% of 160 = 16; "I wouldn't do the number calculation on the exam". (3) Understanding, circles in percent: 10 both, 15 bride only, 75 groom only; it need not be 10: 15% both → 10, 70, 5% neither; max 25% → bride only 0, groom only 60, neither 15 | solve-wp24-g074 (360 guests, 45% artist, 70% owner → 54) | SAME (all 3 ways and every step: 10% method, the complement 30% for 70%, "write the data in order", the free max (now also a trap choice), 115% → 15%, then the 20% and the 45% overlaps with their neither. Her quarter shortcut doesn't fit 45%, so English uses 10% + 5%; her verdict became "one small calculation instead of four, that's why we stay in percent") |
| 6 | בית ספר חקלאי · Farm school: 40 students, 18 orchard, 7 barn, which could be neither (Q, medium+) (her item 75) | 4853-4909 | Neither in a range question is the hard part; (1) complements: not orchard 22, not barn 33; neither = their overlap; max 22 → rule out 25, 32; min 55 − 40 = 15 → rule out 11 → 16. (2) Insight: after the max rules out two, one right answer only → of the two left, one is in the range and the other is too small → the bigger one, 16, no min needed; "not trivial; if not, one more small calculation" | solve-wp24-g075 (52 students, library 24, kitchen 13 → 19) | SAME (both ways, word for word in spirit, including "it takes practice, and if you're not sure, the minimum is one more small calculation". English adds a 3rd way, through the students in at least one place) |
| 7 | חברה – שברים · Company: 1/3 English, 3/4 car, 1/4 teens, 2/5 production, which is not necessarily true (Q, medium) (her item 76) | 4911-5008 | Each choice claims an overlap must exist → check if the two groups go over the whole; (1) fractions, whole = 1: 1/3 + 3/4 = 13/12 > 1 forced; production + **not English (complement 2/3)** = 16/15 forced; teens + car = exactly 1 → not forced (shown with 60 workers: 15 teens, 45 drivers); less than 1 (1/4 + 1/3) → min 0, not negative. (2) Percent: **1/3 → 33%, not 33⅓, because when the sum is far from 100 the third doesn't matter** (only near 100 or 99-and-a-bit does it); 67 + 40, 25 + 75 = 100 → the answer, 40 + 75; "this is what you do on the exam: convert to percent, much faster" | solve-wp24-g076 (nurses: 3/10 nights, 3/4 drive, 1/4 new, 1/2 part time) | CHANGED: both ways, the complements (two of them now), "exactly one is not forced" with a numbers example (20 nurses), "less than one → zero, never negative", and "in the exam, turn the fractions into percent" are all there. **But the English fractions contain no 1/3**, so her rounding tip has nothing to act on: slide 3 still says "For one third, thirty-three percent is only an estimate. Don't round if the sum is close to a hundred", about a fraction that is not in the question |
| 8 | ארוחת צהריים · Lunch: 1/3 rice, 1/5 mash, 1/10 both, 6 people both → neither (Q, medium+) (her item 77) | 5010-5101 | (1) Squares method in fractions (whole = 1): mash only 1/5 − 1/10 = 1/10; not rice 2/3; neither 2/3 − 1/10 = 17/30; then fraction → people with the **triangle value**: 17/30 × 6 ÷ 1/10, multiply by the reciprocal, reduce → 34. (2) Insight: 1/10 = 6 → total 60; rice 20, mash 12 (60 ÷ 5 by splitting 50 + 10), not rice 40; mash only 6; neither 34; "this is the way I want you to work on the exam; check if you can work in percent or find the numbers" | solve-wp24-g077 (conference: 1/4, 1/6, 1/12 both, 4 people → 32) | CHANGED: both ways and her exam advice ("find the total first, and work in people") are kept. In way 1 **the triangle-value step is gone**: with the English numbers neither comes out as 8/12 and both is 1/12, so English says "each twelfth is four people, eight twelfths is 32". Her harder conversion (17/30 vs 1/10, cross-multiply, reciprocal) is not needed with these numbers. Her "60 ÷ 5 = 50 ÷ 5 + 10 ÷ 5" mental-math aside is also gone (48 ÷ 6 needs none). English adds the traps 28 and 16 |
| 9 | ינשופים · Owls: Amir 24, Zehava 18, together 30 different owls → both (Q, medium) (her item 78) | 5103-5171 | (1) Understanding: "together they photographed 30" → no owl is in neither, **neither = 0, implied, not written**; Zehava must take the 6 Amir missed, the other 12 are Amir's → 6, 12, 12. (2) Squares: not Amir 6, neither 0 → Zehava only 6 → both 12. "Quite a few questions have neither = 0; with practice look out for it, it's the box to start from" | solve-wp24-g078 (movie lists 34, 27, 45 different → 16) | SAME (both ways, "it's not written, but it comes from the words"; English adds the count-each-once line 61 − 45 and the trap 11; the "neither = 0" idea is also taught earlier in wp-069 slides 5-6) |
| 10 | 10 שאלות תרגול עצמי · 10 self-practice questions (no video) | 5173 | — | practice wp24-p01 … p10, p13, p16, p17 + q-r26-t24-05, -09, -12 (16 questions) | SAME (her 10 have no subtitle text, so they can't be matched one by one; the English practice set is larger) |

**Count by row (19 rows):** SAME 16 · CHANGED 2 (7, 8) · PARTIAL 0 · MISSING 1 (4, trivial).

### Count by video (her 13 units)

| Unit | Match |
|---|---|
| Intro (67): 1a-1b | SAME |
| Ranges lesson (68): 2a-2e | SAME |
| Exact lesson (69): 3a-3b | SAME |
| Fish (70) | SAME |
| Marina (71) | SAME |
| Economics students (72) | SAME |
| Advanced heading (73) | MISSING (trivial, no spoken text) |
| Q wedding (74) | SAME |
| Q farm school (75) | SAME |
| Q company (76) | CHANGED (the 1/3 → 33% rounding tip no longer has a 1/3 to work on) |
| Q lunch (77) | CHANGED (the triangle-value conversion was replaced by "each twelfth = 4") |
| Q owls (78) | SAME |
| 10 practice questions | SAME |

**By video: SAME 10 · CHANGED 2 · PARTIAL 0 · MISSING 1.**

---

## 2. English → Hebrew (English topic-24 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| wp-067 slide 2 | A second picture of the four regions (red / electric cars) | none | no |
| wp-067 slide 3 | The mistake "10 play music" ≠ music only; a whole group = only + both | only implicit in her fish example (15 − 12 = 3) | no |
| wp-067-2 slide 3 | The pizza again as an exact question (one slice with no topping → exactly 2) | her exact lesson does this with the kids, not the pizza | no |
| wp-067-3 (whole part) | The rule A + B − both + neither = total ("count each one once"), two examples, recap | none: she never uses this formula, only the squares method | no |
| wp-068-2 slide 3 | The total isn't written: 24 hours in a day (two machines) | none | no |
| wp-068-2 slide 4 | Range in percent, stay in percent (60% + 55% → 15%) | her wedding Q (74) way 2, moved forward into the lesson | no |
| wp-068-2 slide 5 | Fractions: the whole is one, and percent is often faster | her company Q (76), moved forward | no |
| wp-068-3 slide 1 | Range of another region (art only at least / gloves only at most) and the "at least ≠ smallest overlap" trap | none | no |
| wp-068-3 slide 2 | Neither as the overlap of the two "not" groups | her farm-school Q (75), moved forward | no |
| wp-069 slide 4 | Start from any box the question gives | none | no |
| wp-069 slides 5-6 | Neither = 0 when the total counts only members (tea/coffee guests, stamps vs a class) | her owls Q (78), moved forward | no |
| wp-069 slide 7 | "Exactly one" = sum − 2 × both | none | no |
| 2nd/3rd ways added in g070, g071 (count each once), g072 (flip rule from t23), g075 (through the students in at least one place), g078 (count-each-once line) + a trap-choice line in every solution | extra methods and traps | none | no |
| solve-q-r26-t24-01 | At least how many swim only (range of a non-overlap region) | none | no |
| r26-t24-two-way + solve-q-r26-t24-02 | Two traits per person, the two-way table; percents of different wholes ("percent of what?") | none | no |
| r26-t24-three-groups + solve-q-r26-t24-03 | Three groups: at least in all three (count who misses each), pairs given, exactly one/two | none | no |
| r26-t24-summary | Replaced by the summary page (summary_pages/t24.json), not read aloud | none | — |
| practice q-r26-t24-05, -09, -12 | Extra practice questions (not videos) | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **Q76: round 1/3 to 33% when the sum is far from 100** (the tip is in the English script, but the English question has no 1/3, so the sentence talks about a fraction the student never sees) | wp24-g076 stem + solve-wp24-g076 slides 0-1, 3-4. E.g. make night shifts **1/3** instead of 3/10: choice 2 becomes 1/3 + 3/4 = 13/12 (33 + 75 = 108, far over 100, so rounding is safe), choice 1 "not nights" becomes 2/3 + 3/4 (67 + 75), choice 4 1/2 + 2/3 (50 + 67). Choice 3 (1/4 + 3/4 = 1) is unchanged | no | **Restore** (about 2 sentences plus new numbers). At the least, cut the orphan "For one third…" line, since right now it is wrong for this question |
| 2 | Q77: turning the "neither" fraction into people with the triangle value (17/30 × 6 ÷ 1/10) | solve-wp24-g077 slide 1 | no | Not needed. With the English numbers "each twelfth is four people" is correct and simpler, and her own exam advice is to skip the fractions anyway (way 2) |
| 3 | Kindergarten example: "most students prefer the formula; strong students just see it" | wp-068-2 slide 2 | no | Not needed (a which-way-is-better verdict, banned by R35) |
| 4 | The advanced heading (item 73) | — | — | Not needed (no spoken content) |
| 5 | Her flow order (wedding, farm, company, lunch, owls) | flow order | — | Not needed; the English order (exact questions first, then ranges) is deliberate |

Nothing of her teaching is lost in the lessons: every method, shortcut and warning she gives in the intro, the ranges lesson
and the exact lesson is in wp-067/068/069, and the insights from her advanced questions were also moved forward into the
lessons. Every topic-24 video is unrecorded, so any fix costs no re-recording.
