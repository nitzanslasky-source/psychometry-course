# Topic 16 (Integers): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 15738-17360 (source 12; all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t16.py`), practice list from the course dump.
- Recording status (`video_status.py`): **done** = consecutive-integers, consecutive-products, solve-q-457/458/459/467/468/469/471/472,
  solve-q-r26-t16-01/02/03, r26-t16-consecutive-sums. **Re-read pending** (recorded, to be read again) = whole-numbers, parity,
  solve-q-460-466, solve-q-470. **Not recorded** = solve-q-r26-t16-04. r26-t16-summary = summary page.

**Match scale.** New numbers alone are not a change. SAME = same idea and all her methods. CHANGED = same idea, method / example
type / order differs. PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Structure and numbering.** Her section has four short lessons, each with worked examples inside: חיובי-שלילי (1 example),
מספרים עוקבים (2 examples), זוגיות (3 examples), מכפלות מיוחדות (2 examples); then 8 advanced questions and 20 practice
questions. English keeps the four lessons as four camera videos (whole-numbers, consecutive-integers, parity,
consecutive-products) and gives each of her 8 in-lesson examples its own solution video (q-457 … q-464); her 8 advanced
questions are q-465 … q-472. No numbering gaps.

**Her names.** הצגה אלגברית → "write the whole group with one letter"; הצבת מספרים → "plugging in"; הבנת הפרשים → "use the
differences / the gaps"; "חזקה לא משפיעה על הזוגיות, מותר למחוק חזקות" → "check the numbers without the powers"; מכפלות מיוחדות →
"products of consecutive integers".

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | חיובי-שלילי: כפל · Signs in multiplication | 15740-15751 | Easy topic "from my experience"; same signs → +, different → −, order doesn't matter | whole-numbers slides 0-1 | SAME (English adds "a positive product doesn't mean both are positive") |
| 1b | ספירת מינוסים · Count the minuses | 15752-15768 | Plus signs don't matter; odd number of minuses → negative, even → positive; every two minuses cancel | whole-numbers slide 2 | SAME |
| 1c | חילוק · Division | 15769-15772 | Same as multiplication, nothing new to remember | whole-numbers slide 3 | SAME (English adds powers, \|x\|, −x and addition, slides 4-5) |
| 1d | a⁴b³/\|b\| < 0 (example) | 15775-15813 | Why b ≠ 0 is given (NITE always protects the denominator, unlike the bagrut); \|b\| > 0; a⁴ > 0 (and a ≠ 0, else the fraction is 0); so b³ < 0 → b < 0 | whole-numbers slide 6 + solve-q-457 (a⁵b²/\|a\|) | SAME ("the not-zero given is there for the bottom of the fraction" kept; English adds a plug-in method) |
| 2a | מספרים עוקבים: 3 דרכים · Consecutive: three ways | 15817-15840 | Definition (also negatives); three ways — algebraic (b−1, b, b+1, or a, a+1, a+2 …), plugging in, differences; "know all three, pick what suits" | consecutive-integers slides 0-1 | SAME (English adds consecutive even/odd, gap 2) |
| 2b | (c² − a²)/b, a<b<c consecutive (example) | 15843-15876 | ">0 doesn't mean they start at 1, a could be 17"; write a and c with b; expand both squares by the formulas; **keep the brackets after the minus**; cancel → 4 | solve-q-458 ((r² − p²)/2q, consecutive **even**) | CHANGED: the example is now consecutive even numbers (gap 2), and the top is opened with the difference-of-squares formula instead of expanding both squares. Her "they don't have to start at 1" is in the lesson (slide 1); her bracket warning survives as "subtract the whole expression q − 2". English adds a plug-in method and the gap-of-one trap |
| 2c | (c−a)/(b−a) − (a−b)/(c−b) (example, plugging in) | 15879-15905 | Plug in 1, 2, 3 ("could be 5, 6, 7, small is easier"); **work out each fraction first, then apply the minus in front** | solve-q-459 slide 0 (four numbers p, q, r, s) | SAME (her warning kept: "if you got zero, check the subtraction between the fractions") |
| 2d | הבנת הפרשים · The same expression by differences | 15906-15945 | Gaps 1, 1, 2; the order of subtraction decides the sign (b − a = 1, a − b = −1) | consecutive-integers slide 1 (end) + solve-q-459 slide 1 | SAME |
| 2e | סיכום עוקבים · Close | 15946-15975 | Three ways recap; differences suit stronger students; plugging in usually recommended | consecutive-integers slide 0 | SAME (the which-way verdict dropped, R35) |
| 3a | זוגי, ו-0 זוגי · Even numbers; zero is even | 15977-16008 | Definition; 0 is even; **memory tip: 7,580 ends in 0 and is even, so 0 must be even** | parity slide 1 | PARTIAL: "zero is even, because zero divided by two is an integer" is there; **her memory tip (numbers ending in 0 are even) is missing** |
| 3b | חיבור וחיסור · Adding and subtracting | 16009-16036 | Even ± even, odd ± odd → even; even ± odd → odd (the two extra 1s make a 2); what "odd" is (not "divisible by 1"); "you don't need to remember, plug in 1 + 2" | parity slide 1 | SAME (her "odd ≠ divisible by 1" aside is not said) |
| 3c | רק האי-זוגיים משפיעים · Only the odd terms count | 16054-16084 | Even terms don't change parity; count the odd ones (2, −6, −4, 8 vs 5, 3, 7) | parity slide 1 | SAME |
| 3d | כפל · Multiplication | 16037-16053, 16085-16109 | One even factor makes the product even (5·7·2·3; 6·13 + 5·14 − 7·9) | parity slide 2 | SAME (English adds the 2(x+7) vs 2x+7 bracket warning) |
| 3e | חילוק · Division rules | 16110-16151 | odd/odd → odd or fraction; even/odd → even or fraction; odd/even → only a fraction (the 2 can't cancel); even/even → anything | parity slide 3 | SAME |
| 3f | 3 הצבות בחילוק · Three plug-ins for division | 16152-16157, 16283-16293 | With division do **three plug-ins of small, close numbers**; "not 100%, but covers 99% of cases" | parity slide 4 + r26-t16-summary slide 3 | CHANGED (deliberately): English says "these show what is possible, not three tests we must do every time"; start with one example, add another only to separate choices, and "working examples alone do not prove always" |
| 3g | חזקה לא משפיעה · Powers don't change parity | 16158-16183 | 2ⁿ stays even, 3ⁿ stays odd → "you may delete the powers" | parity slide 4 | SAME |
| 3h | x+y אי-זוגי, 4y + x^y + y^x + 5 (example) | 16186-16222 | Plug in both cases (y even / x even) → 16, 12; slow, so instead delete the powers → 4y + (x + y) + 5 → odd + odd → even | solve-q-460 (m^n + n^m + 9 + 4n) | SAME (both methods, both cases; English puts the delete-the-powers method first) |
| 3i | 2y/x², x זוגי y אי-זוגי (example) | 16225-16293 | The trap: "even/even can be anything" gives the wrong answer; you must **reduce first**: x = 2k → y/2k² = odd/even → always a fraction; plug in three close pairs (2,1), (2,3), (4,3) | solve-q-461 (6a/b², a odd, b even) | CHANGED: her key lesson (even/even doesn't decide, write the even number as 2k and reduce first) is kept. Her three-plug-in check is replaced by one plug-in plus "examples alone can't prove it, the rule settles it" |
| 3j | x − y = 2, מה בוודאות זוגי (example) | 16296-16323 | Plug in 3, 1 (smallest numbers) and test the choices; understanding (both even or both odd) is possible "but a waste of time" | solve-q-462 (a − b = 6) | SAME (both; English adds why two even numbers wouldn't separate the choices) |
| 3k | סיכום זוגיות · Close | 16324-16330 | Even → 2, odd → 1 or 3; "you can plug in 0 for even, but avoid it, it can zero things out" | parity slide 4, solve-q-464 slide 0 | SAME (the zero warning appears where it matters, in q-464) |
| 4a | מכפלות מיוחדות – הכללים · Special products: the rules | 16332-16357 | 2 in a row → ÷2, 3 → ÷6, 4 → ÷24; two evens → ÷4; three evens → ÷8; two consecutive evens → ÷8 | consecutive-products slides 1-2 | SAME (English gives the reason for each rule; "three evens → 8" is not stated) |
| 4b | "לא צריך לזכור – מציבים את הקטנים ביותר" · Don't memorise, plug in the smallest | 16358-16401, 16494-16502 | Her main point of the lesson: instead of the rules, multiply the **smallest** allowed numbers (1·2, 1·2·3, 1·2·3·4, 2·2, 2·2·2, 2·4, never 0): "what you get is what the product divides by" | r26-t16-summary slide 4 ("the smallest allowed example can rule out choices"), solve-q-r26-t16-04 | PARTIAL: the lesson checks every rule on its smallest example (1·2·3·4 = 24, 2·4 = 8) but never says "you don't need the rules, the smallest product is the divisor". English deliberately weakens it to "the smallest example rules out choices", because the shortcut fails for some products (r26-t16-04: 1·3·5 = 15, yet three odd numbers in a row are only sure to divide by 3) |
| 4c | (x² − 1)/4, x אי-זוגי (example) | 16404-16469 | Plug in 5, 1, 3 → 6, 0, 2, always even; "even/even could be anything, but here it isn't"; the math way: difference of squares → two consecutive evens → 8k → 2k; "very hard, plugging in takes 10 seconds" | solve-q-463 ((9n² − 1)/4) | CHANGED: same two methods, but English uses one plug-in (n = 1) and then says more even results can't tell the choices apart, so the formula settles it, instead of her three plug-ins |
| 4d | (x³ − x)/2 (example) + tip | 16472-16513 | Plug in 1, 2, 3 (odd, even, odd) → 0, 3, 12 → always divisible by 3 ("0 is divisible too"); tip: take out x, then x² − 1, a special product | solve-q-464 ((n − n³)/3) | CHANGED: one smart plug-in (n = 2, because n = 1 gives 0, which fits two choices) instead of her three; her tip (factor into three in a row) is the English 2nd method |
| 5 | a, b, c, d על ציר · Four numbers on a number line, which is negative (Q, medium) | 16520-16618 | Signs by analysis: big − small is positive even for negatives; in parallel plug in −2, −1, 1, 2 for every choice; verdict "depends on the student" | solve-q-465 (w<x<0<y<z) | SAME (verdict dropped) |
| 6 | x<y, xy<0, בהכרח חיובי (Q, medium+) | 16621-16761 | Opposite signs + order → y positive, x negative; three ways for each choice: analysis, simplify first (divide by x, difference of squares, cancel xy), plug in (−1, 1); 0 is neither positive nor negative | solve-q-466 (x>y, xy<0) | SAME (all three ways, the zero point kept) |
| 7 | a>b, a+b+c>0, איזה נתון נוסף (Q, hard) | 16764-16840 | Plug in the choices as extra givens; **start with the choice that leaves only one case** ("NITE tests working smart"), not choice 1 with three cases; a, b negative → c must compensate; disprove the rest with numbers (100, 0, 0) | solve-q-467 (p>q, p+q+r<0) | SAME (her "start where there is only one case" kept) |
| 8 | x,y ו-a,b עוקבים (Q, medium) | 16843-16929 | Difference of squares, the differences are 1, write y and b with x and a, cancel → 2; plug in: **check first that the choices come out different** (1, 1 makes two equal → use 2, 2) | solve-q-468 (two pairs of consecutive **even** numbers → 4) | SAME (every step incl. "check the choices are distinct before plugging"; the pairs are now even numbers) |
| 9 | a² + b² = c², עוקבים, מה יכול להיות הסכום (Q, medium+) | 16932-17044 | Write with b → b² = 4b → b = 0 or 4; **the 3-4-5 Pythagorean triple is the main distractor**: its sum 12 is not offered, the answer is −1, 0, 1 → 0; plug in the answers using "the average of three in a row is the middle" | solve-q-469 (x² + y² = z², asks for x + z) | CHANGED: the algebra, both solutions and the middle-number idea (x + z = twice the middle) are kept, plus "don't divide by y, it could be 0". But the answer is now 8, from 3-4-5, so her trap is reversed: the famous triple is the right answer and the forgotten 0 case doesn't bite. The new trap is 12 = adding all three |
| 10 | x = (a−4)⁴ + (a+3)³ זוגיות (Q, medium+) | 17047-17150 | Three ways: (1) the brackets differ by an odd number → one even, one odd → x odd; (2) delete the powers → 2a − 1, odd; (3) plug in **a, not x** (easier to compute), a = 1 and a = 2 | solve-q-470 ((b−3)² + (b+8)³) | SAME (all three; "choose b, since y depends on b" = her "plug a, not x") |
| 11 | 2a + 1 = מכפלה, מה בהכרח אי-זוגי (Q, hard) | 17153-17206 | 2a + 1 is odd whatever a is; an odd product → every factor odd; powers don't count → x even, y odd, z even | solve-q-471 | SAME (English adds a plug-in check) |
| 12 | a זוגי b אי-זוגי, חלקי 8, אינו בהכרח שלם (Q, hard) | 17209-17356 | Count the 2s: a = 2k, (b+1) even, squared → at least three 2s; a²b² has only two; (a+b)² − (a−b)² = 4ab → 8; (b−1)(b+1) consecutive evens → 8; plug in **the smallest** a = 2, b = 1 ("not 4 or 6"), stop at the first non-integer | solve-q-472 (a odd, b even) | SAME (both methods, and why the smallest values matter: "if b were four, choice four would give 2") |
| 13 | 20 שאלות תרגול עצמי · 20 practice questions | 17360 | — | q-473 … q-492 (20) + alg-extra ×3 + q-r26-t16-06/09/11 | SAME (all 20 kept) |

**Count by row (33 rows):** SAME 25 · CHANGED 6 (2b, 3f, 3i, 4c, 4d, 9) · PARTIAL 2 (3a, 4b) · MISSING 0.

### Count by video (her units)

| Unit | Match |
|---|---|
| Lesson 1 positive / negative (1a-1d) | SAME |
| Lesson 2 consecutive numbers (2a-2e) | CHANGED (first example made "consecutive even") |
| Lesson 3 parity (3a-3k) | PARTIAL (the "ends in 0" memory tip; the three-plug-ins rule was changed on purpose) |
| Lesson 4 special products (4a-4d) | PARTIAL ("don't memorise, the smallest product is the divisor" not taught as such) |
| Q5 … Q8, Q10 … Q12 (seven questions) | SAME |
| Q9 a² + b² = c² | CHANGED (trap reversed) |
| 20 practice questions | SAME |

**By video: SAME 9 · CHANGED 2 · PARTIAL 2 · MISSING 0** (13 units: 4 lessons, 8 questions, the practice set).

---

## 2. English → Hebrew (added in English)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| whole-numbers slides 4-5 | Even/odd powers and signs, \|x\|, −x is "the opposite", adding numbers with different signs | none (powers are implicit in her example) | yes (re-read pending) |
| consecutive-integers slide 1 (part) | Consecutive even / odd numbers (gap 2) | none | yes |
| parity slide 2 (part) | 2(x + 7) vs 2x + 7 | none | yes (re-read pending) |
| consecutive-products slides 3-4 | m²(n + 1)/8 by counting twos; x² − 1 for odd x | her Q12 and example 4c (moved up) | yes |
| 2nd methods in q-457, q-458, q-462, q-464, q-471 | Plug-in / factorising | none | yes |
| solve-q-r26-t16-01 | x<0<y, x + y > 0 → y farther from zero | none | yes |
| r26-t16-consecutive-sums | Counting integers in a range (b − a + 1, with gap 2); b² − a² = a + b for neighbours | none (her Q8 uses the second) | yes |
| solve-q-r26-t16-02 | Sum of 7 consecutive = 7 × middle (and why) | her Q9 "average of three = the middle" | yes |
| solve-q-r26-t16-03 | Sum of 4 consecutive: even, never ÷4 | none | yes |
| solve-q-r26-t16-04 | n(n+2)(n+4) for odd n → only ÷3 (the smallest example 15 misleads) | none | **no** |
| r26-t16-summary | Summary page | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **Zero is even, memory tip:** "you know 7,580 is even because it ends in 0, so 0 itself must be even" | parity slide 1, after "zero is even too", ~2 sentences | yes (re-read pending) | **RESTORE** (cheap; it is her named tip for the most common parity trap, and parity is being re-read anyway) |
| 2 | Special products: "don't memorise the rules, multiply the smallest allowed numbers" | consecutive-products slide 1 or 2 | yes (done) | OPTIONAL, and only with a limit: "for numbers in a row, or for even numbers, the smallest product shows the divisor; check it with a second example". As she says it, it breaks for odd numbers in a row (r26-t16-04), so it must not go in unqualified |
| 3 | Q9: the 3-4-5 triple as the distractor, the answer from the forgotten case (−1, 0, 1) | solve-q-469: rebuild the choices so 8 is not offered and 0 is (e.g. choices 12, 0, 6, 10), then the trap is hers again | yes (done) | OPTIONAL. Her trap is a good one, but it needs new choices, a new script and a re-recording; the English "don't divide by y, it could be zero" already teaches the same lesson |
| 4 | Three plug-ins for every division question | — | — | NOT NEEDED (changed on purpose: the English rule "examples don't prove 'always'" is the correct one) |
| 5 | "Odd doesn't mean divisible by 1"; "three even numbers → ÷8" | parity slide 1; consecutive-products slide 2 | yes | NOT NEEDED (asides) |

**RESTORE list:** (1) the zero-is-even memory tip in parity (recorded, re-read pending, ~2 sentences).
Nothing in the English is wrong compared with her; in two places (3f, 4b) the English is deliberately more careful than her
original, because her shortcut can give a wrong answer.
