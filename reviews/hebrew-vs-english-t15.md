# Topic 15 (Division & Remainder): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 14769-15735 (source 12; all of it read). Her
  divisibility-signs lesson (סימני התחלקות, 14771-14929) is the first part of this section and is included.
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t15.py`), practice list from the course dump.
- Recording status (`video_status.py`): **done** = divisibility-2/-3/-4, solve-q-424/428/429/433/434/436. **Re-read pending**
  (recorded, to be read again) = divisibility (part 1), solve-q-423/425/426/427/430/431/432/435, solve-q-r26-t15-01,
  r26-t15-remainder-tools, solve-q-r26-t15-15. r26-t15-summary = summary page. Nothing is "not recorded".

**Match scale.** New numbers alone are not a change. SAME = same idea and all her methods. CHANGED = same idea, method / example
type / order differs. PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Structure and numbering.** Her section: lesson 1 "divisibility signs" (1 example), lesson 2 "remainder" (3 examples),
10 advanced questions, 20 practice questions. English splits the theory into four camera parts (divisibility, -2, -3, -4) and
gives each of her 4 in-lesson examples its own solution video (q-423 … q-426); her 10 advanced questions are q-427 … q-436.
No numbering gaps.

**Her names.** סימני התחלקות → "divisibility signs"; סיפורי התחלקות → not named in English, described as "many exam word problems
are really about divisibility" (divisibility-2 slide 3); שארית מקסימלית → "the biggest remainder"; הצגה אלגברית → "write it with a
letter" (4k + 3); the shop/bottles story → kept (drinks, 8 shekels).

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | סימני התחלקות: 2, 5, 10 · Signs everyone knows | 14771-14791 | Signs tell you without calculating; 2 = even last digit (376); 5 = last digit 0/5 (330, 2,745); 10 = last digit 0 | divisibility slides 0-1 | SAME |
| 1b | 3 ו-9 · Digit sum | 14793-14803 | Digit sum divisible by 3 (417) / by 9 (765) | divisibility slide 2 (942, 523, 846) | SAME (English adds non-examples) |
| 1c | 4 ו-8 · Last two / three digits | 14804-14835 | Last two digits for 4 (3,524: 3,500 + 24, because 100 ÷ 4); last three for 8 (6,320; 1,000 ÷ 8 = 125); 8 is very rare on the exam and then with friendly numbers (320, 480, 640) | divisibility slide 3 | SAME |
| 1d | 6 ו-15 · Built divisors | 14836-14855 | 6 has no sign: 2 and 3 (162); same technique for any bigger divisor, e.g. 15 = 5 and 3 (330) | divisibility-2 slide 1 (234, 135, 510; 12, 18, 24) | SAME (English adds "the two parts must share no divisor, not 2 × 6", which she teaches in advanced Q3) |
| 1e | 11 | 14857-14876 | Two-digit: same digit twice; three-digit: (1) first two digits minus the last (715: 71 − 5 = 66; 132); (2) outer digits minus the middle = 0 or 11 | divisibility-2 slide 2 (418, 427) | SAME (both techniques; English adds the alternating sum for longer numbers) |
| 1f | סיפורי התחלקות – זברות · Divisibility stories: the zebras (example) | 14877-14908 | "Could be" → we can't know the number, so rule out what it can't be; ¼ of the zebras → divisible by 4 (35, 45 out); ⅕ of those → also by 5; she says "it doesn't matter that it's *of those*, in this wording" → 60 | divisibility-2 slide 3 (why we need signs) + solve-q-423 (⅕ of the class, ⅓ of those) | CHANGED: her "could be → rule out" approach and the sign checks are kept. But English deliberately says the opposite of her aside: "it is the basketball group, not just the whole class, that must be divisible by three", and adds a 2nd method, building the group from the inside (15k), with "multiply the denominators" for nested unit fractions. Her shortcut "divisible by 4 and by 5" only gives the right answer because 4 and 5 share no factor, so the English is the safer statement |
| 1g | סיכום סימני התחלקות · Signs lesson close | 14909-14929 | Not much to memorise; 6 / 15 by parts; 11 is the odd one; exam numbers are usually simple (121, 132); "the next lesson, remainder, is harder, come focused" | divisibility-4 slide 3 | SAME ("come in focused, because remainders are the part that confuses people" kept) |
| 2a | שארית – הגדרה והטעות הנפוצה · Remainder; the common mistake | 14932-14968 | 10 ÷ 3 leaves 1; 4 ÷ 7 leaves 4, not 3 ("not the difference"); the grocery story: bottles at 7 shekels with 30 (2 left) and with 4 (0 bottles, 4 left, "maybe the seller slaps me") | divisibility-3 slides 1-2 (drinks at 8 shekels, 35 and 5) | SAME (English adds the words divisor / quotient) |
| 2b | שמרית והקוביות · Shimrit's towers (example) | 14969-14998 | 3 towers leave 2, 4 towers leave 1 → test the choices: 12, 22 out, 17 ✓; "once a choice fits, mark it, there is only one right answer" | solve-q-424 (stamps: rows of 5 leave 4, rows of 3 leave 1) | SAME (her "stop when one fits" kept; English adds a 2nd method, listing 4, 9, 14 …) |
| 2c | השארית המקסימלית · The biggest remainder | 14999-15023 | x ÷ 5 for x = 1 … 6: remainders cycle; the biggest remainder is always one less than the divisor; ÷10 → 9 | divisibility-3 slide 3 (÷4) | SAME |
| 2d | מקסימום xy של שאריות (example) | 15024-15038 | x = remainder ÷ 5 → max 4, y ÷ 3 → max 2 → 8 | solve-q-425 (÷8 and ÷3 → 14) | SAME (English adds the trap 24 = the divisors themselves, and a listing method) |
| 2e | הצגה אלגברית · Writing it with a letter | 15039-15051 | a ÷ 4 leaves 3 → a = 4x + 3; 4x always divides by 4, the 3 is the remainder | divisibility-4 slide 1 (4k + 3, 15k + 4) | SAME (English adds k = 0) |
| 2f | איזה ביטוי מייצג (example) | 15052-15115 | ÷4 leaves 1: test each expression; (4x + 5)² by the formula, and the **shortcut: look only at the free number squared**; 2nd method plug in, "0 or 1 recommended, small numbers" → x = 0 | solve-q-426 (÷5 leaves 4; (5x + 2)²) | SAME (the free-number shortcut and the x = 0 plug-in kept) |
| 2g | סיכום שארית · Remainder close | 15116-15131 | The 3 ÷ 5 confusion again; for expressions plugging in numbers is quickest, "a very important technique" | divisibility-4 slide 3 | SAME (her plug-in praise is a verdict, R35) |
| 3 | 60% בנים · 60% are boys (Q, medium+) | 15136-15160 | 60% boys → 40% girls → ratio 3 : 2; boys = 3 ratio units → divisible by 3 → digit sums 650, 620 out, 630 ✓ | solve-q-427 (30% play tennis → 540) | CHANGED: the same conclusion (a multiple of 3, digit-sum check), but English gets there through the fraction 3/10 of the club (10k members → 3k players) instead of her boys : girls ratio units. Nothing is missing |
| 4 | מכונת הימורים 9, 7, x · The betting machine (Q, hard) | 15162-15194 | Win 10 = divisible by 3 not by 2; digit sum 16 + x → next multiple 18, then +3 each time (972, 975, 978); keep the odd one → 1 value | solve-q-428 (6, 1, X; 12 tokens = by both → 2 values) | SAME (digit sum, then parity; English also does it in the other order. The "long story, only the payout matters" reading is kept) |
| 5 | אינו מתחלק ב-18 · Not divisible by 18 (Q, hard) | 15197-15264 | No sign for 18: long division is the slow way; deduce from the table like 6; 3 × 6 fails (12 divides by 3 and 6 but not 18) because 6 contains 3; use 2 × 9; all even → digit sum decides; "the same for 15" | solve-q-429 (not divisible by 12: 3 × 4, not 2 × 6) | SAME (her "why 3 × 6 fails" kept as "why not 2 × 6"; all choices pass one test so the other decides — kept) |
| 6 | ישי ושירה · Yishai and Shira, how many multiples (Q, hard) | 15267-15312 | "Divisible by 2 and 3" = by 6; every 2nd number is even, every 3rd ÷ 3 → 1/6 of the numbers vs 1/7 → Yishai right; 1/18 vs 1/20 → Shira right; rule: the smaller the divisor, the more multiples | solve-q-430 (15 vs 17; 21 vs 26) | CHANGED: her fraction reasoning is there, but as the 2nd method. English leads with exact counting (first and last multiple, "last minus first, plus one") and adds the caveat "we can trust the fractions because the range is long; in a short range, count exactly" |
| 7 | c = 7a, a = b/4 – אינה בהכרח נכונה (Q, medium) | 15315-15395 | (1) Algebra: 7 is a factor of c; b = 4a; write the sum with one letter: a + b + c = 12a always; a + b = 5a → not necessarily ÷25; (2) plug in, starting from the harder condition (b = 4 → a = 1, c = 7); verdict "plugging in is much shorter here, but understand the algebra for other questions" | solve-q-431 (c = 4a, a = b/5) | SAME (both methods, starting the plug-in from a = b/5; verdict dropped, R35) |
| 8 | x = 2a³ − 2a · necessarily divides (Q, medium) | 15398-15441 | Take out 2a, a² − 1 by the formula → 2(a−1)a(a+1), three in a row → ÷6 → ÷12; plug in: **not a = 1 (gives 0, every choice divides)** → a = 2 → 12; "one smart plug-in is enough when the choices are numbers" | solve-q-432 (5a³ − 5a → 30) | SAME (the "not 1, it gives 0" warning kept. She says "we learned" the three-in-a-row rule; English builds it here, slide 1) |
| 9 | x = 18a + 6 ÷ 10 (Q, medium) | 15444-15490 | ÷10 → x ends in 0 → 18a must end in 4; plug in the answers by the last digit only (8 × 5, 8 × 2, 8 × 3 = 24 ✓) | solve-q-433 (14a + 6) | SAME (her answer-test is the English 2nd method; English adds a 1st method that finds the allowed last digits of a, 1 or 6) |
| 10 | סער בקזינו · Saar at the casino, 700 coins (Q, medium+) | 15493-15539 | Left = 700 − 6x; solving each equation works, "but there's a simpler way": the amount **lost** (the complement to 700) must divide by 6 → check by 2 and 3 (650, 680, 670 out; 660) | solve-q-434 (900 points, x, 2x, 3x) | SAME (her complement method is the English 2nd method; English adds a faster 1st method, 900 − 6x = 6(150 − x), and the trap 15 that passes only the 3-test) |
| 11 | ינון, הלל ויעל · x ÷ 6 leaves 4 (Q, hard) | 15542-15667 | Three ways: (1) algebra 6k + 4; (2) understanding: when the new divisor is contained in 6 (6, 3, 2) only the remainder matters; 4 is not contained in 6 → you can never know; (3) plug in 10 and 4: "not 100%, but solves it most of the time"; her verdict: understanding first, algebra by default, plugging in as a last resort | solve-q-435 (x ÷ 8 leaves 4; Yuval 2x, Noga x ÷ 4, Itay x ÷ 12) | SAME (all three ways; "working examples alone don't guarantee the claims" kept; her contained-divisor rule is also in divisibility-4 slide 2 and the summary. Verdict dropped) |
| 12 | שלושה מספרים שסכומם ÷3 (Q, hard) | 15670-15731 | Add the remainders; all leave 2 → 6, possible (5, 5, 5); max remainder 2; two ÷3 → the third too; one ÷3 → the others not necessarily (3, 1, 2) | solve-q-436 (sum ÷ 6) | SAME |
| 13 | 20 שאלות תרגול עצמי · 20 practice questions | 15735 | — | q-437 … q-456 (20) + alg-extra ×3 + q-r26-t15-06/09 | SAME (all 20 kept) |

**Count by row (25 rows):** SAME 22 · CHANGED 3 (1f, 3, 6) · PARTIAL 0 · MISSING 0.

### Count by video (her units)

| Unit | Match |
|---|---|
| Lesson 1 divisibility signs (1a-1g, incl. the zebra example) | CHANGED (only the zebra example's "of those doesn't matter" aside was reversed; everything else SAME) |
| Lesson 2 remainder (2a-2g, incl. 3 examples) | SAME |
| Q 60% boys | CHANGED (fraction instead of ratio units) |
| Q betting machine, Q not ÷18 | SAME |
| Q Yishai and Shira | CHANGED (exact counting first, her fractions second) |
| Q c = 7a, Q 2a³ − 2a, Q 18a + 6, Q Saar, Q Yinon/Hillel/Yael, Q three numbers | SAME |
| 20 practice questions | SAME |

**By video: SAME 10 · CHANGED 3 · PARTIAL 0 · MISSING 0** (13 units: 2 lessons, 10 questions, the practice set).

---

## 2. English → Hebrew (added in English)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| divisibility-2 slide 1 (part) | Split a big divisor into parts that share nothing (not 2 × 6) | her Q 18 (moved up) | yes |
| divisibility-2 slide 2 (part) | Alternating sum for 11 in longer numbers | none | yes |
| divisibility-3 slide 4 | The digit sum gives the remainder for 3 and 9, and why | none | yes |
| divisibility-4 slide 2 | Changing the divisor works only if the new divisor divides the old one (15k + 4 ÷ 5; 8 vs 6 fails) | her Q x ÷ 6 leaves 4 (moved up) | yes |
| solve-q-423 slide 1 | Building nested groups (15k); multiply the denominators for ⅕ of ⅓; ½ of ¼ → 8 | none (corrects her aside) | yes (re-read pending) |
| solve-q-430 slides 0-1 | Exact counting of multiples in a range (last − first + 1) | none | yes (re-read pending) |
| 2nd / 1st methods in q-424, q-425, q-428, q-433, q-434 | Listing, reversed order of checks, last-digit derivation, 6(150 − x) | none | yes |
| solve-q-r26-t15-01 | Remainders of a − b, a + b, a·b; negative → add the divisor | none | yes (re-read pending) |
| r26-t15-remainder-tools | Number minus remainder divides exactly; ÷4 and ÷6 → 12k (LCM), not 24k | none | yes (re-read pending) |
| solve-q-r26-t15-15 | x ÷ 6, y ÷ 9 → x + y necessarily ÷ 3; "don't assume x = y" | none | yes (re-read pending) |
| r26-t15-summary | Summary page | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | Q 60% boys: the boys : girls **ratio units** view (3 : 2 → boys are 3 units → ÷3) | solve-q-427 slide 0, 1-2 sentences ("thirty percent play and seventy don't, a ratio of three to seven, so the players are three parts") | yes (re-read pending) | NOT NEEDED. Ratio units are taught later in the study plan (word problems), and the English 3/10 → 3k route teaches the same thing with tools the student already has |
| 2 | Q Yishai/Shira: her fraction comparison as the *first* method | solve-q-430 | yes | NOT NEEDED. It is fully there as the 2nd method, and the English caveat (long range only) is a real improvement |
| 3 | Zebra aside "it doesn't matter that it's *of those*" | — | — | NOT NEEDED, and should **not** be restored: it is true only because 4 and 5 share no factor. The English (q-423) is right to state the general rule |
| 4 | Her method verdicts (Q c = 7a, Q x ÷ 6, lesson 2 close) | — | — | NOT NEEDED (R35) |

**RESTORE list: none.** Every method, shortcut and warning she gives in topic 15 is in the English and works with the English
numbers. The one place where the English says something different from her (q-423's "the inner fraction is of the group")
is a correction of a statement of hers that only works for her particular numbers, not an English error.
