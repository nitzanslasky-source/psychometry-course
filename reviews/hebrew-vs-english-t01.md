# Topic 1 (Algebraic Fundamentals): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 26-640 (sources 1 and 2 and the first notes of
  source 3; all of it read). Her line numbers below are file lines.
- English: topics 1-12 have no reading scripts yet, so the English side is the per-topic dump `scratchpad/ext/course/t01.txt`
  (every video's spoken text) and `q01.txt` (65 practice questions), checked against the base translation `base-v18.html`.
- **Recording status.** Topic 1 is not in `video_status.py` (the tracker covers only the Reading Studio topics), so neither
  `--list record` nor `--list send` lists it. Her older English takes exist for `numbers`, `add-subtract`, `multiply-divide`
  and `order-of-operations` (they are in `real_exam/added_by_nitzan.json`). `fast-calculation`, the r26 lessons and the five
  solution videos have no take. The production plan redoes topics 1-12 LAST (first lesson on camera, the rest AI), so
  every restore below goes into the redo scripts. Nothing needs re-recording now.

**Her structure.** She has three videos, each followed by 5 practice questions with no video between them: (1) definitions,
(2) addition and subtraction, (3) multiplication and division. Order of operations was **written instructions on the page,
not a video**, followed by 5 questions, then 20 summary questions (her notes at lines 165-166 and 634-638). She has **no
solution videos** in this topic, so there are no question methods to compare. English numbers differ from hers on purpose
(memory rule *questions-differ-from-hebrew*), so new numbers alone do not count as a change.

SAME = same idea and every one of her methods. CHANGED = same idea, but the method, the example or the place is different.
PARTIAL = part of her content is missing. MISSING = no English equivalent.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches (every method / tip) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | מבוא לאלגברה · Intro to algebra | 30-42 | Algebra is ~¼ of the quantitative section (~5 of 20), but really runs through everything (equations in word problems and geometry); start with definitions for a shared language | `numbers` slide 1 | SAME |
| 1b | מספר שלם · Integer | 43-48 | Divides into units of 1; not ½, 0.7, 1.3; can be negative (−9); 0 is an integer ("sounds strange") | `numbers` slide 2 | SAME (English adds the exam habit "don't upgrade integer to positive integer") |
| 1c | שבר · Fraction | 50-57 | A non-whole number; can be bigger than 1 (7/2 = 3.5, improper); ordinary vs decimal; decimals rare on the exam but we'll learn them | `numbers` slide 3 (9/4 = 2¼) | SAME (English adds "denominator never zero") |
| 1d | מספר טבעי · Natural number | 58-63 | The term is rare; what matters is "positive integer" (not negative, not 0): 205, 14, 9 | `numbers` slide 4 | SAME (English adds "some books include 0; the question's definition wins") |
| 1e | חיובי / שלילי · Positive / negative | 64-69 | Positive = greater than 0, can be a fraction (2/3, ½, ¼); negative = less than 0, fractions too (−5.5, −¼) | `numbers` slide 5 | SAME (English adds nonnegative / nonzero) |
| 1f | מספרים נגדיים · Opposites | 70-76 | ±2, −7 and 7; their sum is 0; fractions too (½, −½) | `numbers` slide 6 | SAME (English adds "−x is not 'a negative number'" and "0 is its own opposite") |
| 1g | מספרים עוקבים · Consecutive | 77-81 | Integers with difference exactly 1; 0,1,2,3 and also −2, −1, 0 | `numbers` slide 7 | SAME |
| 1h | שארית · Remainder | 82-92 | What's left: 10 ÷ 3 → 1 (3 fits up to 9), 12 ÷ 5 → 2 | `numbers` slide 8 | SAME (same examples; English adds "the remainder is smaller than the divisor") |
| 1i | זוגי / אי-זוגי · Even / odd | 93-117 | Even = integer divisible by 2; can be negative (−6); **0 is even**; her memory tip: 1,358 even (ends in 8), 456, 350 ends in 0, 100 → 0 is an even digit; odd must be an integer (4.5 is neither); −13 odd | `numbers` slides 9-10 | SAME (her tip kept almost word for word on the Zero slide; English adds 2k / 2k+1 and uses ½ instead of 4.5) |
| 1j | אפס · Zero | 118-124 | Integer, even, neither positive nor negative; right = positive, left = negative | `numbers` slide 10 | SAME |
| 1k | מספר ראשוני · Prime | 125-150 | "Just a taste": exactly two divisors, itself and 1; = can't be factored (6 = 2·3, 10 = 5·2, 5 = 5·1 doesn't count, 5 = 2+3 is a sum not a product); 11, 17, 19; 0 and 1 not prime; 2 the only even prime, so all other primes are odd (30 and 6 are divisible by 2) | `numbers` slide 11 (15 = 3·5 as the non-example) | SAME |
| 1l | סיכום · Recap + what's next | 151-163 | Most of this is known; the surprises are 0 even, negatives; next: +, −, ×, ÷, then equations, powers, roots and psychometric question types | `numbers` slide 13 | SAME (English adds the three facts NITE prints in the section instructions) |
| 2a | חיבור וחיסור – פתיחה · Intro | 169-175 | No calculator; the exam's numbers are small and mental, but know the technique in case | `add-subtract` slide 1 | SAME (English adds "fast already? try the questions first") |
| 2b | מספרים מכוונים · Signed numbers | 176-209 | "Fancy name for plus and minus"; 7 + (−4) and 7 − (+4) → minus, 3; **the sign always belongs to the number after it**; 7 − (−4) and 7 + (+4) → plus, 11; rule: same signs → write plus, different → write minus | `add-subtract` slides 2-3 (9 + (−14) on a number line; 6 − (−4)) | SAME (English adds the number line and the warning that "turned into plus" doesn't guarantee a positive answer) |
| 2c | שני שליליים · Two negatives | 210-223 | −7 + (−4): ignore the minus, 7 + 4 = 11, put the minus back → −11 | `add-subtract` slide 4 (−8 − 6) | SAME (English adds the warning about the "two minuses make a plus" slogan) |
| 2d | סדר פעולות בחיבור וחיסור · Any order | 224-252 | No order in + and −; the sign travels with its number (−4 + 7 = +7 − 4); put the bigger number first, bigger minus smaller, the result takes the bigger one's sign (7 − 4 vs −7 + 4) | `add-subtract` slides 2 and 5 | SAME |
| 2e | חיבור ארוך · Column addition | 255-282 | Write vertically, align the ones on the right, digit by digit, "graph paper: room for one digit", carry the 1 (973 + 76) | `add-subtract` slide 6 | SAME (English adds the estimate check) |
| 2f | חיסור ארוך · Column subtraction (borrowing) | 283-325 | Same layout; her story "6 asks its neighbour 5: lend me a ten", the 5 becomes 4, 16 − 9 = 7; then **604 − 235**, the 0 has nothing and borrows from the 6 for the 4 → 369 | `add-subtract` slide 7 (703 − 286, the zero case, her lending story kept) | CHANGED: her first, simple one-borrow example is reduced to one sentence ("Usually that's easy — the neighbour hands over a ten and drops by one"); only the zero case is worked. English adds the check by adding back |
| 2g | סיכום · Recap | 326-340 | Must be automatic ("with eyes closed"); practise on the site; if not enough, the intro-to-quantitative book | `add-subtract` slide 9 | SAME (the book reference is dropped; not relevant to the English course) |
| 3a | סימנים בכפל וחילוק · Sign rules | 348-398 | Same signs → positive (general form a·b and (−a)(−b) = ab; 3·2 and −3·−2 = 6); −a/−b = a/b (−3/−2 = 3/2); different signs → negative (−ab; −3·2 = 3·−2 = −6); **a fraction with a minus on top OR bottom is negative as a whole: −3/2 = 3/(−2)** | `multiply-divide` slide 2 (4·7 = 28); the fraction form is in topic 2, `fraction-basics` "Negative fractions" slide | CHANGED: English gives only number examples (no general a·b form) and says "division follows the same rules"; her point about the minus in the numerator or the denominator moved to topic 2 |
| 3b | אפס בכפל וחילוק · Zero | 399-431 | Anything × 0 = 0 (3, −4, a million); 0 ÷ 3 = 0 explained by cakes (6 cakes for 3 people = 2 each, then 0 cakes = 0 each); 3 ÷ 0 is meaningless (can't share among 0 people); questions always add a condition so the denominator isn't 0 | `multiply-divide` slide 3 | SAME (English skips her 6 ÷ 3 = 2 warm-up and starts at 0 cakes; adds fraction bar = division and the colon sign) |
| 3c | כפל ארוך · Long multiplication | 431-482 | More than the times table; vertical, align right; bottom right digit times each top digit, carry and **add** (not multiply) the carry; second row starts under the tens; add the rows: **23 × 17 = 391** | `multiply-divide` slide 4 (246 × 37) | SAME (English adds the sense check) |
| 3d | כפל בפירוק · Multiplying by splitting | 483-518 | **The same 23 × 17 by splitting**: 23 = 20 + 3 ("times" means 'פעמים'); 20 × 17 → ignore the 0, 2 × 17 = 2·10 + 2·7 = 34, add the 0 → 340; 3 × 17 = 30 + 21 = 51; 391 again, "surprise, the same result"; on the exam this is the way (mostly 1-digit × 2-digit) | `multiply-divide` slide 5 (17 × 8 = 80 + 56) | CHANGED: (a) English splits a different, smaller product (one-digit × two-digit), so her "same exercise two ways, same answer" comparison is lost; (b) her two-digit split with the "drop the zero, multiply, add it back" step for 20 × 17 is not shown here (the drop-the-zero idea does appear later, in Smart division: 7 × 8 = 56 → 70 × 8 = 560, and two-digit splits appear in fast-calculation and q-013) |
| 3e | חילוק ארוך · Long division | 518-554 | Start from the LEFT; 1 ÷ 3 doesn't fit → take 16; 3 fits 5 times (needs the times table: 15); 5·3 = 15, subtract → 1; bring down 8 → 18 → 6; **168 ÷ 3 = 56** | `multiply-divide` slide 6 (3,276 ÷ 7 = 468) | SAME (English adds the cycle label and the check by multiplying back) |
| 3f | חילוק פסיכומטרי – פירוק מספר · Psychometric division (splitting) | 555-599 | Long division is for long ugly numbers, but **"on the psychometric the calculations are always SIMPLE, not always EASY; they don't test whether we're pocket calculators"**; 238 ÷ 7: list the multiples of 7 with a 0 added (70, 140, 210, 280 too big), split 238 = 210 + 28 → 30 + 4 = 34 | `multiply-divide` slide 7 (576 ÷ 8 = 560 + 16 → 72) | SAME (her motto kept word for word; English goes straight to "70 eights are 560" instead of listing the tens-multiples and rejecting the one that is too big; English adds "split the dividend, never the divisor") |
| 3g | סיכום · Recap: times table | 600-626 | Long division: practise "psychometric division" instead; **times table up to 10 × 10 perfectly**; 12 × 12 is not needed: 12 × 9 = 10 × 9 + 2 × 9; don't give up on the table (finger methods only in extreme cases); every small step (3 into 16, 7 × 3, 7 × 8) is the table | `multiply-divide` slide 10 | SAME (12 × 9 = 108 kept; the finger-method aside dropped) |
| 4 | סדר פעולות חשבון · Order of operations (written instructions on the page, not a video) | 636 (note only) | No subtitles: it was text on the page | `order-of-operations` (a full video: four levels, left to right, parentheses, minus before brackets, fraction bar) | CHANGED: a video replaces her written text; her text itself is not in the subtitles file, so its content can't be compared |
| — | Practice: 5 + 5 + 5 + 5 questions and 20 summary questions | 165-166, 634-638 | No solution videos | 65 practice questions (q01.txt) + 5 solution videos | CHANGED (more questions; English adds solution videos) |

**Counts (her teaching parts 1a-3g, plus item 4):** SAME 23 · CHANGED 4 (2f, 3a, 3d, 4) · PARTIAL 0 · MISSING 0.

---

## 2. English → Hebrew (English topic-1 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Her take? |
|---|---|---|---|
| `numbers` slide 5 (part) | Nonnegative, nonzero ("nonzero is not positive") | none | yes |
| `numbers` slide 6 (part) | "−x is the opposite of x, not a negative number"; 0 is its own opposite | none | yes |
| `numbers` slide 8 (part) | The remainder is always smaller than the divisor | none | yes |
| `numbers` slide 9 (part) | Even = 2k, odd = 2k + 1 | none | yes |
| `numbers` slide 12 (whole slide) | Reciprocals ("opposites add to 0, reciprocals multiply to 1"; 0 has none) | none | yes |
| `numbers` slide 13 (part) | The three facts NITE prints in the section's general comments | none | yes |
| `add-subtract` slides 2, 4 (parts) | Number-line picture; the "two minuses make a plus" slogan warning (signs that don't touch) | none | yes |
| `add-subtract` slide 8 (whole slide) | Round numbers (398 + 57 via 400; subtract 200 and give 2 back) | none | yes |
| `multiply-divide` slide 8 | Many negatives: count them, even → positive, odd → negative | none | yes |
| `multiply-divide` slide 9 | Last-digit trick + estimate to kill choices | none | yes |
| `fast-calculation` (whole video, 13 slides) | Shifting sums/differences, ×9 ×11, double & halve, ×25 ×125, near a round number, friendly pairs, cancel first, around a centre, squares ending in 5, swap a percentage, estimate | none (her 3d/3f splitting is the seed) | no |
| `order-of-operations` (whole video) | See item 4: a video in place of her written page | her written text only | yes |
| `r26-t01-exam-words` | Sum, difference, product, quotient; multiples, divisors; digits; distinct, at least / at most; consecutive even/odd | none | no |
| `r26-t01-must-could` | Must / could / cannot, test numbers (0, 1, −1, ½, 10), exam strategy | none | no |
| `solve-q-r26-t01-01, -05, -06, -15, -11` | Five solution videos (digits/distinct; must; cannot; last digit + estimate; minus before brackets) | none (she has no topic-1 solution videos) | no |
| `r26-t01-summary`, `r26-t01-summary-fast` | Summary videos (now replaced by the printable summary page per the plan) | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **3d: the same product solved both ways** (long multiplication, then splitting 23 × 17 = 20 × 17 + 3 × 17, with "20 × 17: drop the zero, 2 × 17 = 34, add it back"; "same result") | `multiply-divide` slide 5: either split the slide-4 product, or add a second split example of two-digit × two-digit before 17 × 8. About 4-5 sentences | her old take exists; the topic is scheduled for the 1-12 redo | **Restore** in the redo. It is her only bridge between the two methods, and the "drop the zero and add it back" step is a skill students use all through the course |
| 2 | 3f: list the tens-multiples of the divisor (70, 140, 210, 280 → too big) to choose the chunk | `multiply-divide` slide 7, before "seventy eights are 560": "Eight, sixteen… add a zero: 80, 160… 560 fits, 640 is too big" (1-2 sentences) | same as above | **Optional.** It answers "how did you know to pick 560?", which a weak student will ask |
| 3 | 2f: the simple one-borrow subtraction before the zero case | `add-subtract` slide 7, one quick example before the zero case (2-3 sentences) | same as above | Optional. English already says it in one sentence; a worked one helps weak students only |
| 4 | 3a: the general letter form (a·b, −a·b) | `multiply-divide` slide 2 | same | Not needed. Topic 1 is numbers-first; letters come in topic 4 |
| 5 | 3a: minus in the numerator or the denominator → the whole fraction is negative | already in topic 2 (`fraction-basics`, "Negative fractions") | — | Not needed (moved, not lost) |
| 6 | 3g: finger methods aside; 2g: the intro book | — | — | Not needed |

Nothing in topic 1 is wrong compared with her. Her named motto ("simple, not easy; not pocket calculators"), her 0-is-even
memory tip, her cakes for 0 ÷ n and n ÷ 0, and her 12 × 9 times-table argument are all kept.
