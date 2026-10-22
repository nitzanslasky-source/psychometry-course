# Topic 2 (Fractions — Fundamentals): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 640-1431 (source 3 after the topic-1 notes; all of
  it read). Her line numbers below are file lines.
- English: topics 1-12 have no reading scripts yet, so the English side is `scratchpad/ext/course/t02.txt` (every video's
  spoken text) and `q02.txt` (63 practice questions), checked against the base translation `base-v18.html`.
- **Recording status.** Topic 2 is not in `video_status.py` (the tracker covers only the Reading Studio topics). Her older
  English takes exist for `fraction-basics`, `fraction-multiply`, `fraction-add` and `decimals` (in
  `real_exam/added_by_nitzan.json`); `r26-t02-shortcuts` and the five solution videos have none. Topics 1-12 are redone
  LAST in the production plan, so every restore below goes into the redo scripts. Nothing needs re-recording now.

**Her structure.** Four teaching videos, each followed by 5 practice questions with no video between them: (1) intro to
fractions, (2) multiplying and dividing, (3) adding and subtracting, (4) decimal fractions; then 20 summary questions (her
notes at lines 640, 900, 1089, 1205, 1431). She has **no solution videos** here. Her one question inside a lesson (2 over
3/4, "answer 4 is correct", 1046-1082) is compared below. New numbers alone do not count as a change.

SAME = same idea and every one of her methods. CHANGED = same idea, different method / example / place. PARTIAL = part of
her content missing. MISSING = no English equivalent.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches (every method / tip) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | מבוא לשברים – פתיחה · Why fractions | 642-648 | Part of the algebra base; needed for equations, expressions, word problems, geometry | `fraction-basics` slide 1 | SAME |
| 1b | שבר פשוט · Simple fraction | 649-688 | Part of a whole: a whole cut in 3 → 1/3; **the fraction bar reads "out of" (מתוך)**; 2/3 = "twice a third"; numerator on top, denominator below; 1/5, 3/5 = 3 × 1/5; **the parts must be equal** | `fraction-basics` slides 2-3 (pizza: 1/4, 3/4 = three copies of 1/4) | SAME (English adds "the denominator is not the unshaded pieces") |
| 1c | שבר מדומה ומספר מעורב · Improper fraction and mixed number | 689-728 | Two circles in thirds: 5/3 = 3/3 + 2/3 = 1 2/3; 3/3 = 1; 7/3 = 2 1/3; improper = numerator bigger than denominator = more than 1; mixed number is another way to write it | `fraction-basics` slide 4 (7/4 = 1 3/4; 8/4 = 2) | SAME (English adds "the 'and' in a mixed number means plus") |
| 1d | ממדומה למעורב · Improper → mixed | 729-750 | How many times the denominator fits into the numerator, the remainder stays on top: 9/2 = 4 1/2, 20/3 = 6 2/3 | `fraction-basics` slide 5 (15/4 = 3 3/4) | SAME (one example instead of two; English adds "the fraction bar is division") |
| 1e | ממעורב למדומה · Mixed → improper | 751-783 | Whole × denominator + numerator, same denominator: 5 2/3 = 17/3, then the check back (3 into 17); 2 4/5 = 14/5 and the check back | `fraction-basics` slide 6 (2 3/5 = 13/5, "count in fifths", check back) | SAME |
| 1f | הרחבה וצמצום · Expanding and reducing | 784-843 | Value doesn't change when top and bottom are multiplied/divided by the same number; circle: 1/4 = 2/8 (why: a quarter of 4 is 1, a quarter of 8 is 2); reducing 4/6 = 2/3 by erasing lines; not only by 2: 1/4 × 3 = 3/12 | `fraction-basics` slides 7-8 (1/2 = 2/4 = 4/8; 3/5 = 12/20; 18/24 = 3/4 in stages) | SAME (English adds "change only one and you change the amount" and reducing in stages; her "a quarter of 4 is 1, of 8 is 2" explanation is not used, the picture carries it) |
| 1g | הבנת מונה ומכנה · Effect of numerator and denominator | 844-891 | Bigger numerator → bigger fraction (4/6 → 5/6, "more pizza slices"); bigger denominator → smaller fraction (4/6 → 4/8, "the harder rule"); her memory picture: **cakes (numerator) shared between people (denominator)** | `fraction-basics` slide 9 (1/4 → 3/4; 1/4 vs 1/6; cakes and people) | SAME |
| 1h | סיכום · Closing | 892-898 | Very important; base for algebra, word problems, geometry (parts of circles, of hours) | `fraction-basics` slide 13 | SAME |
| 2a | כפל וחילוק שברים – פתיחה · Intro | 902-907 | Uses last lesson's reducing; if not solid, go back and practise | `fraction-multiply` slide 1 | SAME |
| 2b | כפל שברים · Multiplying | 908-949 | Top × top, bottom × bottom (3/8 × 4/10); 12/80 is awkward to reduce, so **cancel before multiplying** (4 and 8); allowed only because there is only multiplication, **never with + or −** ((3+4)/(8+10)); cancelling diagonally is fine (3·4 = 4·3); you may cancel even before writing one fraction bar; if you miss it, reduce later | `fraction-multiply` slides 2 and 4 (grid 3/4 × 2/5; cancel first 14/15 × 25/21) | SAME (English adds the area grid, "two fractions below one give a smaller answer") |
| 2c | כפל שבר במספר שלם · Fraction × whole number | 950-964 | Turn 3 into 3/1 ("3 cakes for one child"); 2/5 × 3 = 6/5 = 1 1/5 | `fraction-multiply` slide 5 (6 = 6/1, "six cakes for one person", 7/2 = 3½) | SAME |
| 2d | חילוק שברים – כפל בהופכי · Dividing: multiply by the reciprocal | 965-996 | Why you can't divide tops and bottoms separately (4÷2 and 7÷3 "is not right"); keep the first, ÷ → ×, flip the second; reminder of "reciprocal" from the definitions lesson; **her memory tip: the name "כפל בהופכי" = first multiply, then reciprocal, so flip the SECOND fraction**; cancel 4 and 2 → 6/7 | `fraction-multiply` slide 6 (3/4 ÷ 2/5 → 15/8; "flip only the one after the division sign"; ÷ 5 = × 1/5) | CHANGED: her word-order mnemonic is Hebrew-only and became the plain rule "only the one after the sign, never the first". Her remark that you can't simply divide top by top and bottom by bottom is not said (true sometimes, so leaving it out is fine) |
| 2e | שבר במונה ושבר במכנה · Stacked fraction | 997-1009 | Fraction over fraction looks scary but is the same: 2/3 over 4/5 → 2/3 × 5/4 = 5/6, cancelling early | `fraction-multiply` slide 7 (5/6 over 10/9 = 3/4) | SAME (English adds the "main bar" rule here; she gives it in 2g) |
| 2f | שיטת הקשתות / האוזניים · The arcs ("ears") method | 1010-1045 | Shown only for those who know it; **she strongly recommends against it** (students mix up what goes on top); also shows that not cancelling early is harmless: 10/12 → 5/6 at the end | `fraction-multiply` slide 7 ("just so you've seen it… my advice: skip it") | SAME (her "fine if it's automatic from school" aside dropped) |
| 2g | דוגמה משולבת: 2 לחלק ל-3/4 · Worked question: 2 over 3/4 | 1046-1082 | The **main fraction bar is the longer one, level with the equals sign**; rewrite on one line; 2 = 2/1; × 4/3 = 8/3; could be 2 2/3, **but the answer choices already show 8/3, so stop** | `fraction-multiply` slide 8 "Whole over a fraction" (the same 2 over 3/4) | SAME (her "stop when the choices show it" kept: "If the answers show eight thirds, you're already done") |
| 2h | סיכום · Closing | 1083-1087 | Important technique for many question types later | `fraction-multiply` slide 12 | SAME |
| 3a | חיבור עם מכנה זהה · Same denominator (picture) | 1091-1105 | Rectangles in eighths: 3/8 + 2/8 laid on top of each other = 5/8 | `fraction-add` slide 2 (2/7 + 3/7 bars) | SAME |
| 3b | למה צריך מכנה משותף · Why a common denominator | 1106-1126 | Same-size rectangle cut into 8 and into 6: 3/8 + 2/6 laid on each other gives strips of unknown size, so you can't add; need a common denominator | `fraction-add` slide 2, last two lines (one sentence: "eighths and sixths don't line up") + slide 4 (halves and thirds re-cut into sixths) | SAME (her "doesn't line up" picture is now one sentence, but slide 4 shows the same idea with the re-cut pizzas) |
| 3c | חיסור עם מכנה זהה · Same-denominator subtraction | 1127-1132 | 5/7 − 2/7 = 3/7 | `fraction-add` slide 2 (6/7 − 2/7) | SAME |
| 3d | הרחבת מכנה אחד · Expand one denominator | 1133-1153 | 3/10 + 1/5: 5 reaches 10 by ×2, top too, 2/10 + 3/10 = 5/10 = 1/2 | `fraction-add` slide 3 (the same numbers) | SAME |
| 3e | הרחבת שני המכנים · Expand both | 1154-1180 | 2/3 + 1/5: 3 can't reach 5, so pick 15; **often just multiply the denominators**, sometimes a smaller one exists; ×5 and ×3 top and bottom → 13/15; repeated once | `fraction-add` slide 4 (1/2 + 1/3 = 5/6, "just multiply them") | SAME |
| 3f | חיסור + המכנה המשותף הקטן · Subtraction and the smallest common denominator | 1181-1199 | 3/4 − 1/6: 24 works, 12 is smaller; 24 would also be fine (reduce later); **technique: take the bigger denominator and run through its multiples** (6 no, 12 yes; and for 3, 5: 5, 10, 15) → 7/12 | `fraction-add` slides 5-6 (8 and 12 → 24 via multiples of 12, "96 is fine too"; 5/6 − 1/4 = 7/12) | SAME (English adds the name LCM and "write the sign between the expanded fractions") |
| 3g | סיכום · Closing | 1200-1203 | Basic technique, practise until perfect | `fraction-add` slide 10 | SAME |
| 4a | שברים עשרוניים – פתיחה · Why decimals | 1207-1211 | Rare as a topic, but needed inside other questions (motion problems) | `decimals` slide 1 | SAME |
| 4b | ערך המקום · Place value | 1212-1228 | Whole part, point, fraction part; tenths, hundredths, thousandths; 0.1, 0.03, 0.075 = 75/1000 | `decimals` slide 2 (3.07; 0.4, 0.07, 0.006) | SAME |
| 4c | מעשרוני לפשוט · Decimal → fraction | 1229-1259 | Numerator = the digits after the point; the denominator's zeros = the number of places; why 0.03 has the 0 (3 pushed to the right); denominator always 1 followed by zeros ("really a power of 10, we haven't learned powers"); 0.37 = 37/100 | `decimals` slide 3 (0.36 = 9/25; 1.125 = 9/8) | SAME |
| 4d | מפשוט לעשרוני · Fraction → decimal | 1260-1287 | Bring the denominator to 10, 100, 1000; **50 is a multiple of 10 but not "1 with zeros"** → 7/50 = 14/100 = 0.14; sometimes go DOWN: 3/30 = 1/10 = 0.1 | `decimals` slide 4 (the same 7/50 and 3/30) | SAME (English adds five fractions to know by heart) |
| 4e | אפסים בסוף · Trailing zeros | 1288-1304 | 0.3 = 0.30 = 0.300, shown through the fractions (the zeros cancel); bottom line: cross them out | `decimals` slide 5 (0.5) | SAME (English adds the warning about a zero right after the point) |
| 4f | חיבור וחיסור עשרוניים · Adding and subtracting | 1305-1335 | Like column addition, point over point; subtraction with a borrow; **her shortcut: when it's 0 − 7 with 3 next to it, don't borrow, just see 30 − 7 = 23** | `decimals` slide 6 (point over point; 5.2 written as 5.20, borrow) | PARTIAL: her "read the two digits as one number (30 − 7 = 23) instead of borrowing" shortcut is missing. English adds "write 5.2 as 5.20 so every column has a digit" |
| 4g | כפל עשרוניים · Multiplying | 1336-1363 | Ignore the points, multiply (3.2 × 2.14 → 6,848), count the places in both numbers together (3) → 6.848; **tip: estimate instead of counting (3-and-a-bit × 2-and-a-bit ≈ 6, never 68.48)** | `decimals` slide 7 (1.4 × 0.6 = 0.84; 0.3 × 0.04 = 0.012) | SAME (her estimate tip kept; English adds the leading zero case) |
| 4h | כפל וחילוק ב-10 · × and ÷ by 10 | 1364-1386 | The point moves; × → the number grows → right; ÷ → left; one place per zero (51.72 × 10, 3.015 × 100, 58.9 ÷ 10) | `decimals` slide 8 | SAME |
| 4i | חילוק עשרוניים · Dividing decimals | 1387-1417 | Write as a fraction and expand until whole: 2.8/0.4 ×10 → 28/4 = 7; **6/1.5: ×10 gives 60/15 (harder); smarter: ×2 is enough, 12/3 = 4 — you only need whole numbers** | `decimals` slide 9 (4.8/0.06 ×100 = 80; 0.75/1.5 ×4 = 3/6 = 1/2, "you only need whole numbers, not the biggest ones") | SAME |
| 4j | סיכום · Closing | 1418-1428 | Decimals rare; multiplying decimals rarely needed; you will need adding/subtracting and expanding / ×10 to clear decimals | `decimals` slide 13 | SAME |
| — | Practice: 5 + 5 + 5 + 5 questions, then 20 summary questions | 640, 900, 1089, 1205, 1431 | No solution videos | 63 practice questions (q02.txt) + 5 solution videos | CHANGED (more questions, solution videos added) |

**Counts (her 33 teaching parts 1a-4j):** SAME 31 · CHANGED 1 (2d) · PARTIAL 1 (4f) · MISSING 0.

---

## 2. English → Hebrew (English topic-2 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Her take? |
|---|---|---|---|
| `fraction-basics` slides 10-12 | What cancelling means (factor vs term); splitting the top, never the bottom; negative fractions (minus in front / on top / at the bottom; a minus in front belongs to the whole top) | her topic-1 point "a minus on top or bottom makes the whole fraction negative" (topic-1 lines 389-398) moved here; the rest none | yes |
| `fraction-multiply` slide 3 | "Of" means times; the trap "one third, then a quarter of the REST" | none | yes |
| `fraction-multiply` slides 6 (part), 9, 10 | Dividing by a whole number; mixed numbers (make them improper, never multiply the parts separately); what division means (how many eighths fit into 3/4) | none | yes |
| `fraction-add` slides 7-9 | Whole and mixed numbers in + / −; fraction bar = brackets; mixed operations (order of operations) | none | yes |
| `decimals` slides 10-12 (and recap part) | ÷0.5, ÷0.25, ÷0.2 (and ÷0.125); comparing decimals; 1/3 never ends | none | yes |
| `r26-t02-shortcuts` (whole video) | Estimate with 0, ½, 1; test a rule with easy numbers; the cross shortcut; mixed numbers fast | none | no |
| `solve-q-r26-t02-01, -05, -10, -19, -15` | Five solution videos (split the top; of the remaining; fraction bar = brackets; estimate with ½; ÷0.25 = ×4) | none (she has no topic-2 solution videos) | no |
| `r26-t02-summary` | Summary video (replaced by the printable summary page in the plan) | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | 4f: **subtracting decimals without borrowing — read the digits as one number** (her 30 − 7 = 23) | `decimals` slide 6, after the borrow example: e.g. "Or skip the borrow: forty minus eight is thirty-two" with the English numbers adjusted so the case appears (1-2 sentences) | her old take exists; topic scheduled for the 1-12 redo | **Optional.** It is a real speed tip of hers, but it costs a new number setup; worth adding in the redo |
| 2 | 2d: her mnemonic "כפל בהופכי" (multiply, then the reciprocal → flip the second) | `fraction-multiply` slide 6 | same | Not needed. It is a Hebrew word-order trick; the English "keep, change, flip — only the one after the sign" does the same job. If an English memory aid is wanted, "keep · change · flip" already gives the order |
| 3 | 1f: "a quarter of 4 is 1, a quarter of 8 is 2" as the reason 1/4 = 2/8 | `fraction-basics` slide 7 | same | Not needed; the pizza picture carries the reason |
| 4 | 1d: a second improper → mixed example (she has 9/2 and 20/3) | `fraction-basics` slide 5 | same | Optional (rule: ≥2 examples for a first-time concept); the check-back on slide 6 is a second instance |

Nothing in topic 2 is wrong compared with her. All her named moves are kept: "the fraction bar = out of", the cakes and
people picture, cancel before multiplying (only with ×), the arcs method shown but discouraged, the main bar level with
the equals sign, stop when the choices show the improper form, multiples of the bigger denominator, 50 isn't "1 with
zeros", the estimate instead of counting places, and "expand only enough to get whole numbers".
