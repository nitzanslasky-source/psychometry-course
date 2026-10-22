# Topic 25 (Averages): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/02-Word-Problems-Original-Subtitles.txt`, lines 5175-5921 (all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t25.py`), the base
  translation `studio-build/base-v18.html`, and the practice-question dump `ext/course/q25.txt`.
- Recording status from `python3 video_status.py --list record`: **every topic-25 video is still unrecorded** (wp-080,
  wp-080-2/-3, wp-081, wp-081-2/-3, wp-086, wp-086-2/-3 and all 14 solution videos). Nothing in topic 25 needs re-recording.

**Match scale** (as in the t23 report). English questions have new numbers on purpose, so new numbers alone are not a change.
SAME = same idea and all of her methods. CHANGED = same idea, but the method, example type or order is different. PARTIAL = some
of her content or one of her methods is missing. MISSING = no English equivalent.

**Her video numbering (80-90), no gaps.** 80 = lesson "averages", 81 = "sum from the average", 82 = the gifted-class question,
83-85 = the three advanced questions (Q4, Q17, Q19), 86 = the weighted-average intro, 87 and 88 = the two biology-matriculation
examples, 89 = Q5, 90 = Q17 (the book). The English ids follow the same numbers (wp-080, wp-081, solve-wp25-g082 … g090), so
nothing was merged or dropped. The heading "לימוד מתקדם" (5328) is just a label, not a video. Her 87 and 88 were worked examples
inside her weighted lesson. In English they are try-first questions, and wp-086 teaches the same ideas on new examples first.

**Her method names in English.** נוסחת הממוצע → "the formula" (the average is the sum divided by how many). ממוצע כנקודת איזון →
"the balance" (the average of two numbers is exactly in the middle; the differences add up to zero). הצבת מספרים → "plug in
numbers". ממוצע משוקלל → "weighted average". נדנדה / ציר → "the seesaw / the pivot", "the distances are the weights, flipped".
מגדלי קוביות → "towers of blocks".

**A gap in her own course that English fills.** In Q4 (5362) she says "ההגדרה הראשונה - ממוצע כנקודת איזון" (the first
definition, the average as a balance point), but her lesson 80 never actually says "balance point". It only shows the towers and
"the middle". English teaches the balance explicitly in wp-080-2 slides 3-5, so her later questions now rest on a taught idea.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew · English gloss) | Lines | What she teaches / every method | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | ממוצע חשבוני · What an average is | 5176-5180 | A number that describes the middle of a group; the exam usually says just "ממוצע" | wp-080 slides 0-1 | SAME |
| 1b | קבוצה סימטרית · Symmetric groups | 5181-5194 | 10, 20 → 15; 2, 4, 6, 8 → 5; 2, 4, 6 → 4 (the average can also be one of the numbers) | wp-080 slides 1-2 (16, 30 → 23; 6, 10, 14, 18 → 12) | SAME (English adds evenly spaced numbers, slides 3-4) |
| 1c | כלל ראשון · Rule 1: adding numbers equal to the average | 5195-5205 | 2, 4, 4, 4, 4, 6 is still 4; adding or removing values equal to the average doesn't change it | wp-080 slide 5 (3, 5, 5, 7) | SAME (English adds "adding 12 raises it") |
| 1d | מגדלי קוביות · Cube towers and the limits | 5206-5235 | 12, 5, 4, 8, 5, 3, 6, 5 as towers; "box the average in": not above 12, not below 3, strictly between them; share the blocks → 6 | wp-080-2 slide 1 (4, 9, 3, 11, 8 → 7) | SAME |
| 1e | נוסחת הממוצע · The formula from the towers | 5236-5252 | All the blocks = the sum, the towers = how many; 48 / 8 = 6; "the formula from school" | wp-080-2 slide 2 (35 / 5; and 2, 5, 11) | SAME |
| 2a | סכום = מספר איברים × ממוצע · Sum = how many × average | 5253-5287 | 8 / 2 = 4, so 8 = 2 × 4; we don't need the numbers, treat each one as the average (3 numbers of average 5 → 15, "maybe 6, 8, 3") | wp-081 slides 1-2 (12 / 3 = 4; 4 numbers of average 6; 9 players) | SAME (English checks with real numbers, 2 + 5 + 7 + 10) |
| 2b | כיתת המחוננים · The gifted class (worked question, item 82) | 5289-5324 | 8 students × 6 = 48 puzzles together. **The question asks what Sapir alone CAN'T solve: 49**, since all of them together solve 48. She could solve 48 if the others solve 0, but never 49 | solve-wp25-g082 (12 volunteers × 7 bags = 84) | PARTIAL: the base translation already changed the question to "how many altogether?", so **her "one person can't exceed the total, but can equal it if the others are 0" is lost**. All that is left is "maybe one filled twenty and another two, it doesn't matter" |
| 3 | שאלה 4 · Dani and Sarit's heights (Q, easy) | 5329-5386 | (1) The formula: (171 + S) / 2 = 168, ×2, −171 → 165, +16 → 181. (2) The balance point: Dani 3 above, so Sarit 3 below, "faster and easier" | solve-wp25-g083 (Ethan 169, average 164, +18 → 177) | SAME (both methods, in her order; English adds the trap 182 = average + 18) |
| 4 | שאלה 17 · Sum of the pair averages (Q, hard) | 5389-5494 | (1) Algebra: 3 numbers, 3 pairs, same denominator, take out 2 → x + y + z = 3 × the average. (2) Plug in all 1 ("it doesn't say they're different"), rule out three choices, "I still don't mark it"; "a hard question became a warm-up" | solve-wp25-g084 (4 numbers, 6 pairs → 6 × the average) | CHANGED: 4 numbers and 6 pairs instead of her 3 and 3, so the algebra needs "each number is in 3 pairs" and "sum = 4A". Both methods and her "don't stop at the first match" are kept |
| 5 | שאלה 19 · Guy and Ruti, history and chemistry (Q, hard) | 5496-5611 | (1) Table, G and G + 3, two more unknowns ("I try to avoid them, but I must"), the formula, ×2, G cancels → 11. (2) Plug in: Guy 80 and 80 again ("then the average is 80, no calculation"), Ruti's average 76, the balance point (83 is 7 above, so 69) → 11 | solve-wp25-g085 (Omar and Lena, 6 and 5 → 16) | SAME (both methods, the table, "70 again, so no calculation"; English adds the trap 11 = 6 + 5) |
| 6 | סיכום השיעור · Closing of the advanced lesson | 5612-5624 | "Nothing new; the formula works, but plugging in and the balance point are faster" | none (wp-081-3 slide 3 has its own summary, not this one) | MISSING (trivial; a which-way-is-better verdict, which R35 bans) |
| 7 | ממוצע משוקלל – מבוא · Weighted average intro (item 86) | 5626-5641 | Values with different weights; the heavier one pulls the average; 5 units of math vs 1 unit of language | wp-086 slides 0-1 (a final exam vs a quiz) | SAME |
| 8 | ביולוגיה 3:1 · Biology, exam 3 units 60, lab 1 unit 100 (item 87) | 5643-5740 | "It says average, not weighted, so notice it yourself"; copies: 60 + 60 + 60 + 100, ÷4 not ÷2 → 70; the formula (value × weight, ÷ the sum of the weights); the seesaw: tilted, push the pivot toward the heavy side; distances 10 and 30, 3 × 10 = 1 × 30; the distances are the weights flipped | wp-086 slides 1-3 (Dan, 80 × 3 and 40 → 70) + wp-086-2 slide 1 (the seesaw, 3 × 10 = 1 × 30) + solve-wp25-g087 (61 × 2, 97 → 73) | SAME (every step; English adds a 3-weight example, and the traps 79 and 85 in g087) |
| 9 | ביולוגיה 4:1 · Biology, 100 × 4 and 50 × 1, the exam form (item 88) | 5744-5788 | "As we'd do it on the exam": the axis, values above, weights below, 4 × heavier → 4 × closer, gap 50 into 5 units of 10 → 90 from either end; "it may look strange; with practice it's much faster" | wp-086-2 slide 2 (Noa, 80 × 4 and 30 → 70) + solve-wp25-g088 (91 × 5, 55 → 85) | SAME (English adds the formula as a check, and the trap 61). Only her encouragement "it may look strange at first, with practice it's faster" is gone |
| 10 | שאלה 5 · 5 numbers average 70, 10 numbers average 85 (Q, easy, item 89) | 5791-5860 | (1) The weighted formula, the weight = the group's size, reduce by 3 → 80. (2) "Is it chance? No": 1 × 70 + 2 × 85 gives the same 80; the common factor 5 cancels, so use the weight ratio. (3) **No calculation at all: the middle is 77.5, closer to the bigger group → rule out 1 and 2; "can't be determined" is just a scary choice when everything is given → only 80 is left.** (4) Ratios 1 : 2 flipped, 3 units → 80 | solve-wp25-g089 (8 × 58, 12 × 78 → 70) + wp-086-3 slide 1 (6 × 40, 9 × 50 → 46) | PARTIAL: (1), (2) (why the factor cancels) and (4) are there. **(3) no longer works**: the English choices are 70, 68, 72, 66, so the estimate leaves two choices and the seesaw has to finish it. **Her "can't be determined from the data" choice and how to rule it out are missing** |
| 11 | שאלה 17 · The book, 1,000 lines of 6 or 7 words, average 6¼ (Q, hard, item 90) | 5862-5910 | "Until now they asked for the average; here it's given and they ask for a group's size"; (1) the formula: 7x + 6(1000 − x) = 6250 → 250. (2) The ratios backwards: ¼ and ¾, 3 × closer to 6 → 3 × more lines → 1000 / 4 = 250 | solve-wp25-g090 (2,000 boxes of 3 or 5 kg, 3.4 → 400) | SAME (both methods, her opening line; English adds a 3rd method, "start everyone at the low value", and the traps 1,600 and 500) |
| 12 | סיכום ממוצע משוקלל · Weighted lesson summary | 5911-5918 | Not always in the middle; closer to the heavier group; the formula and the ratios; the weights' ratio is the distances' ratio flipped | wp-086-3 slide 3 | SAME |
| 13 | 20 שאלות תרגול עצמי · Self-practice (no video) | 5920 | — | wp25-p01 … p27 (21 practice questions) + q-r26-t25-06/-07/-09/-11, plus solve-wp25-p18 | SAME |

**Count by row (17 rows):** SAME 13 · CHANGED 1 (4) · PARTIAL 2 (2b, 10) · MISSING 1 (6).

### Count by video (her 12 units)

| Unit | Match |
|---|---|
| 80 Lesson: averages (1a-1e) | SAME |
| 81 Lesson: sum from the average (2a) | SAME |
| 82 Gifted class (2b) | PARTIAL (her "what can't one of them be" point is gone) |
| 83 Q4 Dani and Sarit | SAME |
| 84 Q17 pair averages | CHANGED (4 numbers and 6 pairs) |
| 85 Q19 Guy and Ruti (+ closing, row 6) | SAME (only the trivial closing verdict is dropped) |
| 86 Weighted intro | SAME |
| 87 Biology 3 : 1 | SAME |
| 88 Biology 4 : 1 | SAME |
| 89 Q5 two groups | PARTIAL (solving it with no calculation, and ruling out "can't be determined", no longer work) |
| 90 Q17 the book | SAME |
| Practice | SAME |

**By video: SAME 9 · CHANGED 1 · PARTIAL 2 · MISSING 0.**

---

## 2. English → Hebrew (added; no Hebrew equivalent)

| English video / part | Added content | Recorded? |
|---|---|---|
| wp-080 slides 3-4 | Evenly spaced numbers, numbers in a row, first + last over 2, an even count | no |
| wp-080-2 slides 3-5 | The balance taught explicitly: the differences from the average add up to zero; a missing score; two numbers | no |
| wp-080-3 (whole video) | A base number (97, 102, 104, 99); one value changes; every value changes (+3, ×2, ages, both in order) | no |
| wp-081 slides 3-5 | A number joins: how many there were (the balance), the new average, the newcomer (suitcases) | no |
| wp-081-2 (whole video) | A number leaves; the biggest possible value (positive / whole / different); the smallest possible biggest value; plugging in equal letters | no |
| wp-081-3 (whole video) | The average equals a letter or the difference; the balance with "more / less than" | no |
| wp-086 slide 3 (part) | The formula with three weights (1, 2, 3) and the trap "÷3" | no |
| wp-086-3 slide 2 | Percent shares as weights (70% / 30% of shirts) | no |
| solve-wp25-g090 slide 2 | 3rd method: start everyone at the low value | no |
| solve-q-r26-t25-01 … -05 | A new student joins; the 5th score by the balance; the biggest of six different integers; nine consecutive even numbers; 3a + 2 | no |
| solve-wp25-p18 | Two averages with letters, x − z | no |
| r26-t25-summary | Replaced by the summary page (summary_pages/t25.json), not read aloud | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **Q5: solve it with no calculation, by the estimate.** The middle, "closer to the bigger group", and ruling out "can't be determined from the data" when every number needed is given | solve-wp25-g089: change the wrong choice 72 to "cannot be determined from the information given". The estimate (above 68) then rules out 68 and 66, she rules out "can't be determined" in about 2 sentences, and 70 is left. The seesaw stays as the 3rd method | no | **Restore.** It is her method (3), and the only place in the topic that teaches dismissing the "can't be determined" choice. It costs one choice change and about 2-3 sentences |
| 2 | **Gifted class: one member can't exceed the total** (48 if the others solve 0, never 49) | end of solve-wp25-g082: "So one volunteer alone can't fill more than eighty-four bags. Eighty-four, if the others filled none, but never eighty-five." (Or restore her question form: "Which of these CAN'T be one volunteer's number of bags?") | no | **Restore** (1-2 sentences). It was the point of her question, and it prepares for the biggest-possible-value idea in wp-081-2 |
| 3 | Q4 (4 : 1) encouragement: "it may look strange, we're used to equations, but with practice it's much faster" | solve-wp25-g088 slide 0, after the seesaw | no | Optional. It is close to a which-way-is-better verdict (R35). A neutral version ("It may feel new, but it takes only a few small steps") keeps her reassurance |
| 4 | The advanced lesson's closing ("the formula works, but plugging in and the balance are faster") | end of solve-wp25-g085 | no | Not needed. It has no new content, and it is an R35 verdict |
| 5 | Q17 with 3 numbers (her original) | solve-wp25-g084 | no | Not needed. The 4-number version teaches the same two methods and is a little harder |

Nothing in the English is wrong compared with her: every calculation in the scripts was checked (g083 177, g084 6A, g085 16,
g087 73, g088 85, g089 70, g090 400, wp-081 slides 4-5). No topic-25 video is recorded, so every restore costs no re-recording.
