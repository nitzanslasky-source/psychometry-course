# Audit T28 - Counting possibilities (additions by the 2026-09 fixers)

Source: `math_patches/t28_CHANGES.md`, `math_patches/t28.py`. Real exam: regenerated `real_exam/quant_real.md` (combinatorics 24 q. and factorials 12 q. read in full; probability 24 q. read in full for counting content; keyword searches over all 760). All cited ids re-checked against the regenerated file.
Rule 2 (coordinator): an added method/type that ORIGINAL course questions already need is kept ("orig" = the original question).

Real-exam counting picture: most real "combinatorics" items are logic/extreme-value puzzles. True counting items: 2023_autumn_q2_07 (3 of 4), 2020_winter_q2_06 (2 of 4 types), 2025_winter_q1_02 (handshakes), 2021_spring_q2_16 (shirt × trousers minus same color), 2022_winter_q2_18 (passwords 2³ + 2⁶), 2026_spring_q2_20 (3·3·2), 2024_spring_q1_05 (digits 2,5,5,7,7 with first = last), 2022_autumn_q1_16, 2024_winter_q2_16, 2020_autumn_q1_16 (listing), 2025_autumn_q1_03 (keys and doors), 2020_spring_q1_07 (divisible by 2 or 7); plus in the probability group 2024_autumn_q1_07 (7! arrangements with Sunday not in place = all − forbidden) and 2019_winter_q1_07 (two people in two ADJACENT chairs in a row). No road-map, zero-digit, mailbox, round-table, unnamed-groups or "at least one" counting question.

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| Q14 video: start with the most restricted digit (hundreds) | solve-wp28-g141 slide 2 | FIX | KEEP | - |
| Q17 video: check sentence, "stays out" | solve-wp28-g144 slides 2-3 | FIX | KEEP | - |
| "Two-Way Connections" → "Mutual Action" | wp-131 title / slide 1 | FIX | KEEP | - |
| "Rare" removed ("Why learn it" slide; "very hard, very rare") | wp-134 slide 2; wp-137 slide 2 | FIX | KEEP | - |
| Q12/Q17 intro lines ("Question twelve/seventeen") | solve-wp28-g139, -g144 | FIX | KEEP | - |
| Q11 cancelling shown as a fraction | solve-wp28-g138 slide 2 | FIX | KEEP | - |
| ÷ for ":", spelling, spaces, TeX, reworded stems (Q3, Q15, p06, p16, p18, p20, p21, p24, p25) | many | FIX | KEEP | - |
| "Not" / "at least one" → all − forbidden (extra line) | wp-134 slide 4 | METHOD | KEEP | 2024_autumn_q1_07 (7! − 6!), 2021_spring_q2_16 (all − same color); orig wp28-g136 |
| "Who stays out" general rule C(n,k) = C(n,n−k) | wp-137 slide "Who stays out"; mem-counting row "k out of n" | METHOD | KEEP | 2023_autumn_q2_07 (3 of 4 = the 1 who stays out); orig wp28-g139 |
| Slide "Groups with no names" (÷2) | wp-137 new slide | CONTENT | REMOVE | 0 real; no original needs it (orig g138 and p27 are NAMED groups) |
| Slide "The checklist" (5 steps) | wp-137 new slide; mem-counting table "The 5-step checklist" | METHOD | KEEP | 2020_winter_q2_06 (group → divide), 2025_winter_q1_02 (counted twice ÷2), 2024_spring_q1_05 (restriction first) |
| mem-counting tips: small-case test; elimination by size | mem-counting tips | METHOD | KEEP | 2025_winter_q1_02 (small case), 2020_winter_q2_06 (group → the smaller choice 6, not 12) |
| Guided Q13: 6 friends into two unnamed groups of 3 | q-r26-t28-01 + solve-q-r26-t28-01 | CONTENT | REMOVE | 0 |
| NEW VIDEO r26-t28-cases slide "Road maps" (and = ×, or = +, drawn map) | r26-t28-cases slide 2 (+ slide figure) | CONTENT | REMOVE | 0 counting-route questions (2022_winter_q1_06 is a probability path tree; 2021_autumn_q1_19 is cutting roads, not counting); no original |
| - slide "The zero trap" | r26-t28-cases slide 3 | CONTENT | REMOVE | 0 real (no digit set with 0); no original needs it (orig p24 uses 1-5) |
| - slide "At least one" (all − none) | r26-t28-cases slide 4 | METHOD | KEEP | 2024_autumn_q1_07 (complement counting), 2025_winter_q2_14 (at least/one of two = 1 − none) |
| - slide "Which is the base?" (objects into boxes) | r26-t28-cases slide 5 | CONTENT | REMOVE | 0 mailbox/boxes questions; no original (codes with repetition are already taught, e.g. orig g128) |
| - slide "Quick checks" (small case; size elimination) | r26-t28-cases slide 6 | METHOD | KEEP | 2025_winter_q1_02, 2020_winter_q2_06 |
| - Recap slide | r26-t28-cases slide 7 | - | KEEP only the "at least one" and "quick checks" lines | - |
| Guided Q19 road map with figure (23) | q-r26-t28-02 + solve-q-r26-t28-02 (+ figure) | CONTENT | REMOVE | 0 |
| Guided Q20 four-digit even numbers from 0-4 | q-r26-t28-03 + solve-q-r26-t28-03 | CONTENT (zero trap) | REMOVE | 0 |
| Guided Q21 codes with at least one 5 | q-r26-t28-04 + solve-q-r26-t28-04 | METHOD (complement) | KEEP | 2024_autumn_q1_07 |
| Guided Q22 5 letters into 3 mailboxes | q-r26-t28-05 + solve-q-r26-t28-05 | CONTENT | REMOVE | 0 |
| NEW VIDEO r26-t28-arrange slide "Together: glue" | r26-t28-arrange slide 2 | CONTENT | KEEP (rule 2) | 2019_winter_q1_07 (two people in adjacent chairs, weak: 1); orig wp28-p23 (two books together) |
| - slide "Not together" (all − together) | r26-t28-arrange slide 3 | METHOD | KEEP (rule 2) | complement as 2024_autumn_q1_07; orig wp28-p15 (no two adjacent) |
| - slide "No two side by side" (gaps) | r26-t28-arrange slide 4 | CONTENT | KEEP (rule 2) | 0 real; orig wp28-p15 |
| - slide "Identical items" (÷ factorial of repeats) | r26-t28-arrange slide 5 | CONTENT | KEEP | 2024_spring_q1_05 (digits 2,5,5,7,7); orig wp28-p25 (LEVEL) |
| - slide "Round table" ((n−1)!) | r26-t28-arrange slide 6 | CONTENT | KEEP (rule 2) | 0 real; orig wp28-p26 |
| - Recap slide | r26-t28-arrange slide 7 | - | KEEP | - |
| Guided Q23 3 math books together | q-r26-t28-06 + solve-q-r26-t28-06 | glue | KEEP (rule 2) | 2019_winter_q1_07; orig p23 |
| Guided Q24 two girls not side by side | q-r26-t28-07 + solve-q-r26-t28-07 | gaps / not together | KEEP (rule 2) | orig p15 |
| Guided Q25 BANANA | q-r26-t28-08 + solve-q-r26-t28-08 | identical items | KEEP | 2024_spring_q1_05; orig p25 |
| Guided Q26 round table, glued pair | q-r26-t28-09 + solve-q-r26-t28-09 | round table | KEEP (rule 2) | orig p26 |
| mem-counting row "Groups with no names" | mem-counting table 2 | CONTENT | REMOVE | 0 |
| mem-counting-advanced table "More methods": rows "Road map", "A zero among the digits", "Objects into boxes" | mem-counting-advanced | CONTENT | REMOVE | 0 |
| - rows "At least one", "Must be together", "Must not be together", "No two side by side", "Identical items", "Round table" | mem-counting-advanced | per slides | KEEP | as above |
| mem-counting-advanced tips "A route may use the direct road too…", "Digits with a zero…" | mem-counting-advanced tips | CONTENT | REMOVE | 0 |
| Practice 10 road map round trip | q-r26-t28-10 | road map | REMOVE | 0 |
| Practice 11 road map (home → stops) | q-r26-t28-11 | road map | REMOVE | 0 |
| Practice 12 three-digit odd from 0-5 | q-r26-t28-12 | zero trap | REMOVE | 0 |
| Practice 13 three-digit from 0,2,5,7,8 | q-r26-t28-13 | zero trap | REMOVE | 0 |
| Practice 14 committee with at least one woman | q-r26-t28-14 | at least one | KEEP | 2024_autumn_q1_07 |
| Practice 15 PIN with at least one repeated/given digit | q-r26-t28-15 | at least one | KEEP | 2024_autumn_q1_07 |
| Practice 16 4 students choose 3 clubs | q-r26-t28-16 | objects into boxes | REMOVE | 0 |
| Practice 17 5 questions × 4 choices (4⁵) | q-r26-t28-17 | code with repetition (original type) | KEEP | 2022_winter_q2_18 (2³ passwords); orig g128 |
| Practice 18 three sisters together | q-r26-t28-18 | glue | KEEP (rule 2) | orig p23 |
| Practice 19 two books not next to each other | q-r26-t28-19 | not together | KEEP (rule 2) | orig p15 |
| Practice 20 7 chairs, no two people adjacent | q-r26-t28-20 | gaps | KEEP (rule 2) | orig p15 |
| Practice 21 digits 1,1,2,2,2 | q-r26-t28-21 | identical | KEEP | 2024_spring_q1_05 |
| Practice 22 digits 0,3,3,5 | q-r26-t28-22 | identical (+ leading digit) | KEEP | 2024_spring_q1_05 |
| Practice 23 round table, not together | q-r26-t28-23 | round table | KEEP (rule 2) | orig p26 |
| Practice 24 8 players into two unnamed teams | q-r26-t28-24 | unnamed groups | REMOVE | 0 |
| Practice 25 6 students into 3 unnamed pairs | q-r26-t28-25 | unnamed groups | REMOVE | 0 |
| Practice 26 8 of 10 | q-r26-t28-26 | who stays out | KEEP | 2023_autumn_q2_07 |
| Practice 27 4-letter code containing A | q-r26-t28-27 | at least one | KEEP | 2024_autumn_q1_07 |

## TO REMOVE
- wp-137 "Choosing a Group": slide "Groups with no names" (and its sidebar entry).
- Guided q-r26-t28-01 + video solve-q-r26-t28-01 (unnamed groups).
- Video r26-t28-cases: slides "Road maps" (2, with its road-map figure), "The zero trap" (3), "Which is the base?" (5); the matching Recap lines ("Road map…", "zero…", "Objects into boxes: each object chooses") and sidebar entries. Rename the video (title "Roads, Zeros and "At Least One"" no longer fits).
- Guided q-r26-t28-02 (+ figure) + solve-q-r26-t28-02; q-r26-t28-03 + solve-q-r26-t28-03; q-r26-t28-05 + solve-q-r26-t28-05.
- Practice q-r26-t28-10, -11, -12, -13, -16, -24, -25.
- mem-counting table 2 row "Groups with no names".
- mem-counting-advanced "More methods" rows "Road map", "A zero among the digits", "Objects into boxes"; tips "A route may use the direct road too — count every path from start to end." and "Digits with a zero: the leading digit is never 0, so split by where the 0 goes."

## ORIGINAL ITEMS REMOVED BY FIXERS (restore - originals stay)
Questions removed (unplaced):
- wp28-p04 (six-digit IDs from 1-6, 6!)
- wp28-p07 (four prizes to four finalists, 4!)
- wp28-p13 (six keys / six cupboards, worst-case tests) - note: this is the same type as REAL 2025_autumn_q1_03 (three keys / three doors, max attempts); calling it "not counting" was wrong on the evidence too.

Questions whose content was replaced: none (only rewording: wp28-g126, g142, p06, p16, p18, p20, p21, p24, p25).

Slides whose original script/title was overwritten:
- wp-131 slide 1 title "Two-Way Connections" → "Mutual Action" (video renamed).
- wp-134 "Add or Subtract Cases" slide 2 "Rare and hard" → "Why learn it" (script replaced); slide 4 line "Subtracting possibilities is even rarer." replaced.
- wp-137 "Choosing a Group" slide 2 line "…Very hard, and very rare." replaced; slide 4 "n−1 out of n" → "Who stays out" (script replaced); Recap slide script replaced.
- solve-wp28-g138 (Q11) slide 2 "Method 1 · Choose, then divide by 4!" script replaced.
- solve-wp28-g141 (Q14) slide 2 "Method 1 · Option counts per digit" script replaced.
- solve-wp28-g139, solve-wp28-g144 intro "Last question of the set." replaced; solve-wp28-g144 slide 2 "Worried you missed one? …" and slide 3 "…who stays in place" replaced.
Memory cards: mem-counting and mem-counting-advanced only had rows/tables added (no original row removed).
