# Topic 22 (General word problems and ratios): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/02-Word-Problems-Original-Subtitles.txt`, lines 1072-2683 (all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t22.py`, flow order =
  its `ORDER`), the base translation `studio-build/base-v18.html`, and the practice list in the course dump `ext/course/q22.txt`.
- Recording status comes from `python3 video_status.py --list record` (unrecorded) and `--list send` / `--list done` (recorded).
  **Not recorded yet: only wp-027 (part 1).** **Recorded:** wp-027-2, wp-027-3, wp-028, wp-031, wp-034, wp-037, g029, g030,
  g032, g033, g035, g036, g038, q-r26-t22-01, q-r26-t22-03 (done); wp-039, g039, g040, r26-t22-shortcuts, g042-g050,
  q-r26-t22-20, r26-t22-exam-tools, q-r26-t22-04, q-r26-t22-05 (recorded, waiting to be sent). So every restore below means
  re-recording part of a recorded video, except anything that goes into wp-027 part 1.

**Match scale** (as in the topic-23 report). English questions use new numbers on purpose (rule *questions-differ-from-hebrew*),
so new numbers alone are not a change. SAME = same idea and every one of her methods. CHANGED = same idea, but a method, the
example type or a claim is different (the cell says what). PARTIAL = some of her content is missing (the cell says what).
MISSING = no English equivalent.

**Her names carry over.** תרגום בעיה מילולית → "translate the words into an equation", 3 שלבים → "three stages", יחסים זהים →
"equal ratios", טבלת יחסים → "the ratio table", יחס אופקי / אנכי → "across / down", ערך משולש → "the triangle value", כפל באלכסון
→ "cross-multiplying", יחידות יחס → "ratio units", קשתות → "arcs", "תן למסכן" → "give it to the little guy", הצבת תשובות → "plug in
the answers", הצבת מספרים → "plug in numbers", הערכת סדר גודל → "estimate", הברקה → "insight", התחלה מהסוף → "start from the end".

**The video numbers.** The ids follow her order: 027 = lesson 1, 028 = lesson 2 (its two worked examples became the try-first
questions g029 and g030), 031 = lesson 3 (its two examples = g032, g033), 034 = lesson 4 (its two examples = g035, g036), 037 =
lesson 5 (its examples = g038, then "give it to the little guy" = wp-039 + g039, then the inequality = g040), **041 = her short
"advanced learning" intro** (2156-2164), 042-050 = her nine advanced questions. Gaps: **031, 034, 037 have no g-question**
because those numbers are the lessons themselves; **039** is used twice (wp-039 = the technique part of her lesson 5, g039 = the
age question that carries it); **041** had no video in the base (the base dropped her intro and put the reference card
mem-general-advanced at the end of the section instead); the current course restores it as **r26-t22-shortcuts**. Her lesson 1
is a camera lesson split into three parts (wp-027, wp-027-2, wp-027-3).

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | תרגום בעיה מילולית למשוואה – פתיחה · Why word problems matter | 1073-1091 | 5 of 20 questions, a quarter, really more, since many algebra/geometry questions are written in words (the remainder example) | wp-027 slide 0 | SAME |
| 1b | שלושת השלבים · The three stages | 1092-1109 | (1) translate to an equation, the hard part, (2) solve, technical, (3) answer what was asked (x = 8 but they ask x − 1 or 2x, "not fair, but stay focused"); not every problem needs an equation (trial and error, plugging in) | wp-027 slide 1 | SAME |
| 1c | דוגמה: סכום הספרות · Example: ×3 + 20 = 5× the number, sum of digits | 1110-1170 | Translate phrase by phrase; "every equation is a sentence", she reads the equation back in words; solve 3x + 20 = 5x → x = 10; stage 3: sum of digits = 1; recap of the 3 stages, "be solid on the algebra basics" | wp-027 slides 2-3 (×3 + 24 = 7×, asks for twice the number; plus a 2nd example x + 15 = 4x, asks x − 1) | SAME (the stage-3 twist is "twice the number" instead of "sum of digits"; English adds a second, shorter example and names the trap) |
| 1d | טבלת ניסוחים · The phrase table | 1171-1258 | A greater by 3 than B (A = B + 3); B smaller by 5 (B = A − 5), the two are the same written the other way; כפול = always ×2, like half = always 2 parts; B smaller by ¼ than A → B = ¾A (the estate is the whole); the difference is 12 → **written with absolute value**, \|A − B\| = 12, "we don't care who is bigger"; מהווה → replace with "is", "of" = times; 2B = 3P "the way I hear it", "like" = equals; ratio 2:3 → 2x, 3x (separate lesson) | wp-027-2 slides 1-3, wp-027-3 slides 1-3 | CHANGED: everything is there, but **the difference is taught as "bigger minus smaller, two cases"**, and the absolute-value bars are only mentioned as "a topic we'll learn later" (her explanation leaned on \|A − B\|). English adds: check every phrase with a number, "four times" vs "four more", "a quarter of what?", a third less. Her side remark "מהווה usually won't appear on the exam" is gone (trivial) |
| 1e | סיכום השיעור · Lesson summary | 1259-1276 | Work step by step, don't run, don't panic at long text — "the biggest tip"; go over the phrase table | wp-027-3 slide 4 (+ the memory card) | SAME |
| 2a | יחסים זהים – פתיחה · Equal ratios intro | 1278-1288 | A very important technique for the whole section (geometry, algebra, word problems) | wp-028 | SAME (English adds what "the same rate" means: pens per box, a steady machine) |
| 2b | 5 תבניות 30 עוגיות · 5 trays, 30 cookies → 20 trays | 1289-1348 | Many solve it in their head (÷5 = 6) or with 5x = 30; the ratio table; across ×6; down ×4; both give 120; "when the ratio is whole, you see it at once" | solve-wp22-g029 (8 vases 56 roses → 12 vases; warm-up 3 boxes 12 pens → 10) | SAME (across ×7 and down ×1.5 instead of two whole ratios; English adds "check which direction is easier" and a warm-up on easier numbers. In her course this was a worked example; English makes it a try-first question) |
| 2c | ירדן, 6 דקות 15 תרגילים · Yarden, 6 min 15 exercises → 8 min | 1349-1439 | Strong students see ×2.5; otherwise the triangle value: multiply the diagonal, divide by what's left, why it's called a triangle; reduce first (15/6 → 5/2); then cross-multiplying 6x = 120; "I personally recommend the triangle value, it writes the missing number at once; but choose what's comfortable"; closing: whole ratio → just multiply, not whole → triangle | solve-wp22-g030 (cook, 18 potatoes in 12 min → 20 min; + apples 4 kg = 14 → 6 kg) | SAME (both methods, reduce-first, the name's reason, and her reason for the triangle value: "it writes the answer straight away, cross-multiplying builds an equation first". Only her personal "I recommend" was dropped, by the R35 no-verdict rule. English adds the bigger-or-smaller check that rules out 36 and a second triangle example) |
| 3a | בעיות חישוב והבנה – פתיחה · Reading-comprehension problems intro | 1441-1453 | Some questions only test reading; lots of information to see if you panic | wp-031 | SAME (English adds what to watch: per 100 g, "or part", what is asked) |
| 3b | פיצה משפחתית · Family pizza: cost vs price | 1455-1513 | Don't skip long text, step by step; dough 100 g → 400 g ×4 (equal ratios again), cheese, 2 tomatoes at ½; total 28; 49 − 28 = 21 | solve-wp22-g032 (café sandwich) | SAME (English adds the trap: 35 = the cost itself is a choice) |
| 3c | חברה א' / ב' – "או חלק ממנה" · Phone companies, "or part of a minute" | 1515-1559 | 22.5 min: 22×2 + 2 for the half = 46; 20 min = 30 + another 15 for the 2.5 min = 45; difference 1; the catch is "or part of" | solve-wp22-g033 (bike shops) | SAME (English adds the rule "round up to the next whole unit" and a vans example) |
| 4a | יחס מתמטי – מה זה יחס · What a ratio is | 1561-1654 | Everyday "tall compared to me" vs math ratio; pens:pencils 2:5, 5 is 2.5× 2; a ratio is a fraction (the colon = divide); read in order; expand/reduce, write reduced; **a ratio gives no amounts** (20 and 50, 10 and 25); you know amounts only when one is given; so write 2x and 5x | wp-034 slides 1-3 (beads 3:7, 2⅓×; + a worked total 50 → 15, 35) | SAME (English adds a numeric example with a given total) |
| 4b | התאמת יחידות יחס בניסוחים · Matching ratio units in different wordings | 1655-1751 | Gili drank 3/5 → Gili 3x, bottle 5x, numerator = first; Aviv 2.5× Gefen → Gefen = x (the smaller, no messy fraction) → ×2 → 2x : 5x; boys:girls 4:7 and the **arcs** trick; **"this wording almost never appears on the exam (so as not to confuse dyslexic students); when it does, the order is obvious (the elder son is bigger)"**; 4 peaches cost like 5 bananas → reversed: pick a value both reach, 100 (25 and 20), or better the common multiple 20 → peaches 5, bananas 4 | wp-034 slides 2, 4-6 (Dan 2/5 of the bottle + what's left 3x; Ann 2.5× Ben → 2x : 5x; arcs; 3 mugs = 8 plates via 24) | CHANGED: (a) **English states the opposite of her exam claim**: "The exam writes ratios this way, the ratio between the red beads and the blue beads, so always match the names to the numbers in order" (the base translation still had her version, "the exam avoids that wording"). The real exams support the English: quant_real.md line 2216, "the ratio between the number of nurses and the number of head nurses is 3 : 2, and the ratio between the number of head nurses and the number of secretaries is 7 : 4", where the order matters. (b) The reversed ratio goes straight to the common multiple (24); her first try with "any value both reach, like 100" was dropped. Everything else is there |
| 4c | 2/7 מהכיתה בנים · Boys are 2/7 of the class: what could the difference be? | 1753-1801 | "The more common exam form: a fraction of something else"; boys 2x, class 7x, girls 5x; difference 3x → must divide by 3 → 12; and boys ÷ 2, girls ÷ 5, class ÷ 7 | solve-wp22-g035 (swimmers 5/12 of campers; difference 2x → even → 22) | SAME (every step, including the divisibility of each part and the total; English adds "the ratio must be fully reduced" and checks that 22 really works) |
| 4d | אופנוע ומכונית 4:7 · Motorbike : car 4:7, difference 12,000 → total | 1803-1843 | 3x = 12,000 → x = 4,000; the total is 11x = 44,000; "even if I swapped 4 and 7, the difference stays 3 and the sum 11" | solve-wp22-g036 (sofa : piano 3:10) | SAME (incl. "the order didn't even matter" and the warning "x is not the answer") |
| 4e | סיכום יחס · Ratio summary | 1844-1869 | Ratio = fraction, read in order (rare on the exam), no amounts, but divisibility of parts/sum/difference — "this does appear on the exam" | wp-034 slide 6 recap; divisibility in g035 | SAME (the recap line about divisibility is in g035, not in the lesson recap) |
| 5a | בניית משוואה או ביטוי – פתיחה · Building an equation or expression | 1871-1882 | Needed everywhere: word problems, algebra, geometry (an area = difference of two areas), even charts | wp-037 | SAME |
| 5b | 5 חדרים, חדר הוסב למחסן · 5 rooms, one becomes a storeroom, +2 each | 1884-1924 | Slowly: 5 rooms × x; in reality 4 rooms × (x + 2); the number of workers didn't change → 5x = 4(x + 2) → x = 8; check what x is | solve-wp22-g038 (8 rows of chairs, one removed, +3 each) | SAME (her equation and the "same total" reason; English adds 2 more methods: the insight "the removed row was shared out, 7 × 3 = 21" and plugging in the answers, and the trap 24 = the new number per row) |
| 5c | טיפ: x = מה שמחפשים · Tip: let x be what they ask for | 1925-1939 | Most of the time; but always check at the end (2x? x − 1?) | wp-037 slide 1, g038 slide 0 | SAME |
| 5d | "תן למסכן" – אורי וירון · "Give it to the little guy": Uri 4 years older, 3 years ago twice | 1942-2087 | Yaron = x (asked, smaller, no minuses); **stop before the equation, add a row "3 years ago"** (x − 3, x + 1); "twice" → many double Uri, but it's the opposite: think of 4 and 8, double the small one → 2(x − 3) = x + 1 → 7; plug in the answers (11, 5, 8 out; checks 7 "just to see"); tip for sharp students: a gap of 4 and "twice" can only be 4 and 8 | wp-039 (the technique as a short intro: Maya twice Tom) + solve-wp22-g039 (Maya 9 years older, 5 years ago twice) | SAME (all four parts: x choice, the extra row, give it to the little guy with 4 and 8, plugging in, and her 4-and-8 insight as "one part = the gap"; English adds "the gap never changes, only the ratio" and the trap 9 = Tom 5 years ago. English moves the technique into its own short intro video before the question) |
| 5e | יוחנן, 50 ₪, 4 בקבוקים אבל לא 5 · Yohanan: 50 enough for 4 bottles, not 5 | 2090-2122, 2129-2147 | An inequality instead of an equation: 4B ≤ 50 → B ≤ 12.5 (rules out 2 choices); 50 < 5B → B > 10 (rules out 9); then plugging in the answers (9: 45 still fits 5 bottles; 12: 48 / 60 ✓) | solve-wp22-g040 (Dana, 105 credits, 6 tickets but not 7) | SAME (both methods. English is more careful than her wording: she said "B < 12.5" after "4B ≤ 50"; English says "at most 17½" and "bigger than 15, not equal", and its choice 15 tests exactly that edge. English adds "you may skip the second inequality but not the second condition") |
| 5f | סיכום בניית משוואה · Summary | 2123-2154 | Read, work step by step; any equation question can also be solved by plugging in the answers; "the stronger students run to the equation, the weaker ones often prefer plugging in" | g040 slide 3 last line | SAME (the "you can almost always plug in the answers too" line is kept; her strong-vs-weak remark was dropped, R35) |
| 6 | לימוד מתקדם – בעיות כלליות · Advanced intro (item 41) | 2156-2164 | General problems have no formula (unlike motion, percents, work); build an equation, understand, or calculate | r26-t22-shortcuts | SAME (the base had dropped it; the current course restores it and adds "almost every question here has a psychometric shortcut; try it yourself first") |
| 7 | מנגו, תפוחים, שזיפים · Gold coin: 1 mango / 2.5 apples / 6 plums (Q, easy) | 2166-2211 | (1) Equal ratios: the easy fruits first; 4 apples by the triangle value 4×1/2.5; clear the decimal by ×2 (×10 works but makes it longer) → 8/5 → 5⅗. (2) Estimate: more than 1 coin for the apples → > 5 (2 choices out); 2 coins = 5 apples > 4 → < 6 | solve-wp22-g042 (kiwis, pineapples, limes) | SAME (both methods, and her "×2, not ×10" remark) |
| 8 | קורס חובלים 128, 7/8 · Cadets: 128, 7/8 stay after each stage (Q, easy+) | 2213-2267 | Draw a bar in 8 parts; 7/8 of 128: reduce by 2 in steps, **"or better, learn to split the number: 128 = 80 + 48, ÷8 = 10 + 16"**; second stage starts at 112 (112 = 80 + 32 → 14 × 7 = 98); the "little insight": write the whole exercise first, 128 × 7/8 × 7/8 = 128/64 × 49 = 98 | solve-wp22-g043 (video game, 160 players, ¾ stay) | PARTIAL: the bar, the "level two starts from the new number" point and the write-the-whole-exercise insight are there (English adds the trap 80 = taking the quarter of 160 twice). **Her number-splitting technique for dividing (128 = 80 + 48) is missing**: with 160 ÷ 4 English just halves twice, so it is not needed with these numbers |
| 9 | בנות = 4/5 מהבנים · Girls = 4/5 of the boys: what fraction of the room? (Q, easy) | 2269-2297 | (1) G = 4/5 B → G/B = 4/5, a ratio is a fraction; or match the units (numerator → first); (2) plug in 5 boys → 4 girls → 4/9 | solve-wp22-g044 (coaches 5/8 of trainees → 5/13) | SAME (both methods; English adds the trap 5/8 and the line "5 to 8 compares the groups, 5 out of 13 compares with everyone") |
| 10 | אפרסקים לייצוא ולשוק המקומי · Export peaches 3× local; 1/3 and 1/4 rejected (Q, medium) | 2299-2358 | (1) Plug in numbers: 1 and 3 fails (¼ of a peach) → change the numbers: a multiple of 4, the smallest → 4 and 12 → 5/16. (2) Estimate: between 1/4 and 1/3 → rules out 3 choices | solve-wp22-g045 (loaves, 2×; ½ and ⅕ whole-wheat → 2/5) | SAME (both methods, the "we chose the numbers, so we may change them" step; English adds the general rule "the mix always lands between the two fractions") |
| 11 | זוהר, מטבעות כסף וזהב · Zohar's coins: gave 1/7 and 1/5, left 8 and 18 in unknown order (Q, very hard) | 2360-2447 | (1) Try both options: 18 = 4/5 of gold → 18 ÷ 4 not whole → impossible; so 18 = 6/7 of silver → 3 per seventh → 21; 8 = 4/5 of gold → 10; 31. (2) Estimate: 26 left, he gave a little → a bit more than 26; 27 impossible (at least one coin from each pile); 52 would mean giving half; 156 even more | solve-wp22-g046 (cupcakes, sold ⅓ and ⅙, left 10 and 14 → 33) | CHANGED (method 1 the same. Method 2 keeps "a bit more than what's left" but makes it exact: "she sold at least a sixth of all → 26 is out; at most a third of all → 48 and 72 are out", instead of her "at least one coin each" and "52 = giving half") |
| 12 | גן א' וגן ב' · Kindergarten A = 2× B; 2 children move; B = 3/5 of A (Q, medium) | 2449-2502 | (1) Equation: x + 2 = 3/5(2x − 2), brackets, ×5 → x = 16 → total 3x = 48 (not x). (2) Divisibility insight: total ÷ 3 (2 choices out), after the move ÷ 8 (3 + 5) → 48, "without calculating anything" | solve-wp22-g047 (buses, A = 4× B, 6 move, B = ½ A → 45) | SAME (both methods; the total doesn't change when children move; English adds "use a fully reduced ratio" and the trap x = 9) |
| 13 | אריאל, דמי כיס ומטלות · Ariel's pocket money: fixed + per chore (Q, easy+) | 2504-2566 | (1) Two equations, subtract → 4M = 120 → 30. (2) Plug in the answers: start with the 8-chore month; 50 → 400 > 290 so 50 and 60 out; 30 → fixed 50 in both months ✓. (3) Insight: 4 more chores = 120 more → 30 | solve-wp22-g048 (plumber: fee + per hour → 45) | SAME (all three methods, including "start with the smaller count" and "too big → the bigger choice is out too") |
| 14 | 6 תפוחים ו-10 בננות · 6 apples + 10 bananas = 800 g; 9 apples + 15 bananas? (Q, medium+) | 2568-2627 | First the idea: apple + banana = 10 doesn't give each, but 2 + 2 = 20 does, 2 apples + 1 banana doesn't; (1) both grew ×1.5 (+50%) → 1,200; (2) divide all by 2 (3, 5, 400) then ×3 → 1,200 | solve-wp22-g049 (9 large + 6 small crates = 240 kg; 12 + 8 → 320) | SAME (the idea with all three cases and both ways; "grew by a third" stands in for her "+50%") |
| 15 | אשר ובטי, 48 סוכריות · Asher and Beti, 48 candies, 8 moved, now equal (Q, medium+) | 2629-2680 | (1) Two equations A + B = 48, A − B = 16, add → 32, 16 → 2. (2) Start from the end: equal → 24 each, "go back in time" (Back to the Future) → 32 and 16 | solve-wp22-g050 (Noa and Eli, 70 stickers, 15 moved) | SAME (both methods and the closing rule; her film joke is gone) |
| 16 | 30 שאלות תרגול עצמי · 30 self-practice questions (no video) | 2682 | — | wp22-p01 … p30 in the practice section, plus p34, p35, p37 and q-r26-t22-06, -15, -16 | SAME (all 30 kept, with new numbers; p31-p33 and p36 of the base are not in the current list) |

**Count by row (32 rows):** SAME 28 · CHANGED 3 (1d, 4b, 11) · PARTIAL 1 (8) · MISSING 0.

### Count by video (her 16 units)

| Unit | Match |
|---|---|
| Lesson 1 תרגום בעיה מילולית למשוואה (1a-1e) | CHANGED (the difference is taught as "bigger minus smaller" instead of through absolute value; nothing missing) |
| Lesson 2 יחסים זהים (2a-2c) | SAME |
| Lesson 3 בעיות חישוב והבנה (3a-3c) | SAME |
| Lesson 4 יחס מתמטי (4a-4e) | CHANGED (her "the exam avoids the 'ratio between A and B' wording" is reversed, correctly; the reversed ratio skips her "pick 100" step) |
| Lesson 5 בניית משוואה או ביטוי (5a-5f) | SAME |
| Advanced intro (item 41) | SAME |
| Q mango (42) | SAME |
| Q cadets (43) | PARTIAL (the number-splitting technique for dividing is missing) |
| Q girls 4/5 (44) | SAME |
| Q peaches (45) | SAME |
| Q Zohar's coins (46) | CHANGED (the estimate reasoning was made exact) |
| Q kindergartens (47) | SAME |
| Q Ariel (48) | SAME |
| Q apples and bananas (49) | SAME |
| Q Asher and Beti (50) | SAME |
| 30 practice questions | SAME |

**By video: SAME 12 · CHANGED 3 · PARTIAL 1 · MISSING 0** (16 units including the practice set).

---

## 2. English → Hebrew (English topic-22 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| wp-027 slide 3 | A 2nd, shorter translation example (x + 15 = 4x, asked x − 1) | none | no |
| wp-027-2, wp-027-3 (parts) | Check each phrase with a number; four times vs four more; "a quarter of what?"; a third less | none | yes |
| solve-wp22-g029 slide 0 | Warm-up ratio table on easy numbers (3 boxes, 12 pens) | none | yes |
| solve-wp22-g030 slides 0, 2 | The bigger-or-smaller check before calculating; a 2nd triangle-value example (apples) | none | yes |
| solve-wp22-g033 slide 1 | "Or part of" = round up; the vans example | none | yes |
| wp-034 slide 3 (part) | A worked total (3x + 7x = 50) | none | yes |
| solve-q-r26-t22-01 | Chained ratios with a shared group (2:3 and 4:5 → 8:12:15), the 2:3:5 trap | none | yes |
| solve-q-r26-t22-03 | A ratio that changes (5:4 → 5:6 after 10 boys leave): make the unchanged part equal | none | yes |
| solve-wp22-g038 slides 1-2 | 2 extra methods: the insight (the removed row was shared out) and plugging in the answers | none | yes |
| solve-q-r26-t22-20 | Shelves: each moved item changes the gap by 2; to make equal give half the gap | none (related to her Q50) | yes |
| wp-039 | "Give it to the little guy" as its own short intro before the age question | her technique, taught inside Q Uri/Yaron | yes |
| solve-wp22-g039 slide 0 (part) | "The gap never changes, only the ratio" | none | yes |
| solve-wp22-g045 slide 2 (part) | The rule "a mix lands between the two group fractions" | implicit in her estimate | yes |
| r26-t22-exam-tools | When an answer cannot be determined (2a + 3p = 13, two pairs give different answers) | her Q49 idea, extended | yes |
| solve-q-r26-t22-04 | Letters in the question and choices (pens and notebooks): plug in numbers, not 0 or 1 | none | yes |
| solve-q-r26-t22-05 | Cars and motorcycles: assume they are all one kind | none | yes |
| solve-q-r26-t22-02 | Worker-days (inverse proportion) | none | withdrawn from topic 22 (taught in topic 26) |
| r26-t22-summary | Replaced by the summary page (summary_pages/t22.json), not read aloud | none | — |
| practice wp22-p34, p35, p37, q-r26-t22-06, -15, -16 | Extra practice questions (not videos) | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **Q43: splitting a number to divide it** ("128 = 80 + 48, so ÷8 is 10 + 16"; "better, in my eyes, than reducing by 2 in steps") | solve-wp22-g043 slide 0. With the English 160 ÷ 4 it isn't needed; it would need a number like 144 or 168 (÷8 → 80 + 64 or 80 + 88), so the numbers would have to change | yes (send) | **Optional.** It is a useful mental-arithmetic habit, but nothing in this question needs it now, and adding it means new numbers and a re-recording. If the teacher wants it, a better home is the arithmetic tools in the algebra topics |
| 2 | Lesson 4: "the 'ratio between A and B is 4:7' wording almost never appears; when it does, the order is obvious" | wp-034 slide 2 | yes (done) | **Not needed — the English is right and hers is out of date.** The real exams use exactly this wording where the order matters (quant_real.md 2216: nurses : head nurses = 3 : 2, head nurses : secretaries = 7 : 4). The teacher should know the English says the opposite of her Hebrew on purpose |
| 3 | Lesson 1: the difference written as absolute value \|A − B\| = 12 | wp-027-3 slide 1 | yes (done) | Not needed. English says "bigger minus smaller, two cases" and points to the absolute-value topic, which comes later in the study plan |
| 4 | Lesson 4: for "4 peaches cost like 5 bananas", first try any value both reach (100), then the common multiple (20) | wp-034 slide 6 | yes (done) | Not needed; English goes straight to the common multiple, which is her own better choice |
| 5 | Q46: her estimate arguments ("at least one coin from each pile → 27 is impossible"; "52 = double, he'd have to give half") | solve-wp22-g046 slide 2 | yes (send) | Not needed; the English choices are different and its "at least a sixth / at most a third of all" version is the same idea made exact |
| 6 | Her verdicts: "I personally recommend the triangle value" (lesson 2) and "stronger students run to the equation, weaker ones prefer plugging in" (lesson 5) | g030, g040 | yes | Not needed: the R35 no-verdict rule; her reason for the triangle value is kept |
| 7 | Small asides: "מהווה usually won't appear", the Back to the Future joke (Q50), "this reminds you of the concentrations question" (Q46), checking choice 4 "just to see" (Q Uri) | — | — | Not needed (no teaching content) |

**Nothing to RESTORE.** Every one of her methods, named techniques ("give it to the little guy", the triangle value, the arcs,
"change the plugged-in numbers", divisibility from ratio units, start from the end, write the whole exercise first) and warnings
is in the English course and still works with the English numbers. The only lost technique (number splitting in Q43) isn't needed
with the English numbers, and the one place where English disagrees with her (the exam's ratio wording) is the English being right.
All of the topic except wp-027 part 1 is recorded, and nothing missing belongs in wp-027 part 1.
