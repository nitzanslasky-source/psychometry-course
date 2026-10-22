# Topic 14 (Prime Numbers): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 13685-14765 (source 12; all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t14.py`), practice list from the course dump.
- Recording status (`video_status.py`): **done** = primes, primes-3, solve-q-387/390/391/401, solve-q-r26-t14-01.
  **Re-read pending** (recorded, to be read again) = primes-2, prime-tools, solve-q-386/388/389/392-400/402, r26-t14-more-tools,
  solve-q-r26-t14-03. r26-t14-summary = summary page. Nothing in the topic is "not recorded".

**Match scale.** New numbers alone are not a change. SAME = same idea and all her methods. CHANGED = same idea, method / example
type / order differs. PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Structure and numbering.** Her topic: an intro lesson (with 2 worked examples), a lesson on factors (1 example), a lesson on the
greatest divisor (2 examples), a lesson on breaking and building numbers (5 examples), 7 advanced questions, 20 practice
questions. English keeps the theory as three camera parts (primes, primes-2, primes-3) and turns each of her 10 in-lesson
examples into its own solution video. **The numbering gap** (q-386-390, then q-398-402, then q-391-397) is not a drop: q-391-397
are her 7 advanced questions, and q-398-402 are her 5 "break and build" lesson examples, numbered after them. The English flow
plays them in her order (386-390, 398-402, 391-397). Her two lessons "greatest divisor" and "break and build" no longer exist as
separate videos: prime-tools says "each of these tools we'll learn inside the question that uses it", and her explanations moved
into q-389, q-390 and q-398-402 (checked below: nothing was lost).

**Her names.** גורם / מחלק "replace divisor with factor, it's the same" → kept word for word (primes-2 slide 2); המחלק המשותף הגדול
ביותר → "the greatest common divisor"; המחלק הוודאי הגדול ביותר → "the greatest number that is guaranteed to divide"; פירוק והרכבת
מספרים → "break a number apart / build numbers" (prime-tools slide 1); ראשוני בריבוע → "a prime squared".

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | מבוא – הגדרה · What a prime is | 13687-13713 | Natural, >1, not a product of two smaller naturals; "divides only by itself and 1"; 13, 11 don't break; 10, 8, 6 do | primes slide 1 (17, 19, 11, 7 / 14, 9, 21, 16) | SAME |
| 1b | 1 ו-2 · One and two | 13714-13727 | 1 is not prime; 2 is the only even prime, every other even number divides by 2 (20, 18) | primes slide 2 | SAME (English adds 0 and negatives, and the odd-sum rule, which she teaches in advanced Q1) |
| 1c | x<15<y, 2 primes between (example) | 13731-13766 | Write the whole numbers, mark the primes; x ∈ {8,9,10} (not 7: prime), y ∈ {20,21,22}; smallest product = smallest x × smallest y = 160 (largest would be 220) | solve-q-386 (x<40<y) | SAME (English explains why 41/43/47 are prime, and uses the "largest product" as a trap choice) |
| 1d | ניסוי וטעייה: x³ דו-ספרתי · Trial and error | 13767-13788 | Try primes against the condition: 2³=8 no, 3³=27 yes, 5³=125 no → 5x=15 | solve-q-387 (x⁶ two-digit, 9x) | SAME (trial kept; English stops early once a power is too big, and adds plugging in the answers and the "they ask for 9x, not x" trap) |
| 1e | סיכום המבוא · Intro summary | 13789-13810 | Know the primes up to 40 by heart (run through 30-40: 31, 37), 97 = largest two-digit prime | primes slide 3 | SAME (English adds 20-30) |
| 2a | גורמים / מחלקים · Factors = divisors | 13812-13826 | Divisor = factor (20 ÷ 4, 30 ÷ 6); "whenever you see divisor, replace it with factor" | primes-2 slide 2 (28 ÷ 4, 45 ÷ 9, 6 ∤ 28) | SAME |
| 2b | גורם ראשוני · Prime factors and combinations | 13827-13866 | Prime factor; a number divides by every combination of its prime factors (12 → 2, 3, 4, 6, 12); every non-prime is a product of primes (60 = 2·2·3·5) | primes-2 slide 3 (28, 20, 18) + primes-3 slide 1 (180 by a factor tree) | SAME |
| 2c | x = 2·5³·6², which is NOT a divisor (example) | 13867-13904 | Not a divisor = can't be built from x's primes; break each choice: 10 ✓, 15 ✓ (3 hides in 6), 30 ✓, 35 ✗ (no 7) | solve-q-388 (x = 3·5²·10²) | SAME (her "6 hides a 3" = English "the twos hide in the tens"; English adds a 2nd method, computing x and dividing) |
| 2d | סיכום גורמים · Factors summary | 13905-13919 | Recap; 60 divides by 4, 6, 10 | primes-3 slide 3 | SAME |
| 3a | המחלק המשותף הגדול ביותר · GCD | 13921-13967 | Two wordings exist (common / guaranteed); "hard for many students, I'll make them simple"; GCD = **take out a common factor**: picture x + y and see what is in both → a·c²·d | prime-tools slide 0 + solve-q-389 slide 0 | SAME ("picture x plus y and take out what's in both" kept; English adds the LCM trap, a numeric example 172/112, and a choices method) |
| 3b | המחלק הוודאי הגדול ביותר · Greatest guaranteed divisor | 13968-14058 | The biggest divisor of a known number is itself (20, 300), so the question is "the biggest one we know is there"; divisible by 9 and 12; why: 2 and 5 → surely 10, but 2 and 6 → not surely 12 (6 itself); **"cancel" a prime that appears in both** (it may be the same 3) → 3·3·2·2 = 36 | solve-q-390 (10 and 25 → 50) | SAME (her "3 and 3·?" logic with 3&7 → 21 but 3&9 not 27; "when there's an overlap we don't count it twice". English phrases the result as "every prime at its higher power" and adds the smallest-number (LCM) method and GCD·LCM = product. Her "the biggest divisor of 20 is 20" opener is not said) |
| 3c | סיכום · Lesson close | 14059-14068 | GCD is just a common factor; guaranteed = cancel the shared prime; "a bit more practice and it'll work" | r26-t14-summary slide 5 | SAME |
| 4a | פירוק והרכבת מספרים – פתיח · Break and build | 14070-14075 | Primes build every number; questions break or build | prime-tools slide 1 | SAME |
| 4b | 4 ספרות מ-1 עד 4, מכפלה (example) | 14077-14108 | Break each choice into primes; a prime outside the allowed digits (40 = 2·2·2·5) can't be the product | solve-q-398 (digits 1, 3, 5 → 30 needs a 2) | SAME (English adds a parity method) |
| 4c | xy = 24, a = \|x−y\| (example) | 14112-14144 | Break 24 into pairs, max − min of the difference = 8; "the story around it is reading comprehension, really it only asks: can you break 24" | solve-q-399 (xy = 100, neither is 1) | SAME (her "long story, underneath just breaking a number" kept; English adds the stop-at-the-root rule and the forgotten 10×10 trap) |
| 4d | סכום המכפלות של 2, 3, 5 (example) | 14145-14164 | Build: 6, 10, 15 and don't forget 2·3·5; add, starting from the big one → 61 | solve-q-400 (cards 2, 5, 7 → 129) | SAME (her "add from the big one" and "don't forget all three" kept; English adds a quick estimate method) |
| 4e | x² ראשוני · x² is prime (example) | 14167-14198 | x² can't break, so x isn't whole; plug in x²=3, 7 → √3, √7; trap "x is prime too" | solve-q-401 (m² prime) | SAME |
| 4f | חלוקה סימטרית · Divisors come in pairs | 14199-14226 | 10 and 12 divide symmetrically (1·12, 2·6, 3·4); a prime squared has a middle divisor with no partner (9: 3; 25: 5) | solve-q-402 slide 0 (18, 16) | SAME (English generalises to "an odd number of divisors means a perfect square") |
| 4g | 3 מחלקים, a = √x (example) + close | 14228-14267 | Exactly 3 divisors → prime squared (other numbers have an even count); √ of it is prime → 2 divisors; close: "the most important lesson; spotting 3 divisors = prime squared saves a lot of time" | solve-q-402 slides 1-2 | SAME (English adds a plug-in method, k = 4. Her "most important lesson" remark is not said) |
| 5 | a+b ראשוניים, איזה לא יכול להיות סכום (Q, medium+) | 14272-14324 | Brute force "would take forever, not fit for the exam"; every exam question has one simple idea; all choices odd → one prime is 2; subtract 2 and test (37 = 2 + 35 ✗) | solve-q-391 | SAME (her "one simple idea, the token drops" kept almost word for word) |
| 6 | בדיוק 2 מתחלקים ב-a, אחד ב-b (Q, medium+) | 14328-14418 | (1) Break all six numbers into primes, find the prime in exactly 2 / exactly 1; (2) plug in the answers (split each choice into two primes and test); her verdict: standard is recommended | solve-q-392 | SAME (both methods; verdict dropped, R35) |
| 7 | ab + 2a = 28, a<b (Q, medium+) | 14421-14463 | "Not obvious where to start, start with what you can": take a out → a(b+2) = 28; factor pairs (not necessarily prime), a is the smaller → sums 27, 14, 9 → the 4th | solve-q-393 (ab + 4a = 48) | SAME (English explains why a is the smaller factor and adds a 2nd method, testing 17 directly) |
| 8 | x = a^c·b^d, necessarily divides (Q, hard) | 14466-14566 | (1) Understanding: an exponent is a count, not a factor (c is not in x); enough copies; (2) plug in the smallest primes in order (2,3,5,7); "when plugging in, knock out 3 before marking — it may hold only for this case"; "if you can do it without plugging in, great; if not, plugging in is excellent" | solve-q-394 (z = p^s·q^r) | SAME (both methods and the "knock out three first" rule kept; English adds the trap "r and s look like factors") |
| 9 | abc ÷ 10 – necessarily not true (Q, hard) | 14569-14657 | 10 = 2·5 → someone brings each prime; one number may hold both (10,1,1); "if a, b odd, c² ÷ 4" (who brought the 2?); different prime divisors of x² = of x (same primes, twice as many copies) | solve-q-395 (abc ÷ 35) | SAME (every statement type kept with 5·7; English states the rule "a prime can't be split between factors" and adds a plug-in method. The stem wording is now "not necessarily true", and English explains that "never true" also counts) |
| 10 | a: 3,5 only; b: 3,7 only; a>b; min ab/35 (Q, medium+) | 14660-14703 | Minimum = each as small as possible: 15, 21; a must be bigger → grow a; not ×2 (only 3s and 5s) → ×3 (smaller than ×5) → 45; cancel → 27 | solve-q-396 (2,3 / 2,5; b<a; ab/15) | SAME (English adds the traps and plugging in the answers from the smallest) |
| 11 | 1<a<99, exactly 3 divisors, how many a (Q, hard) | 14706-14761 | (1) The rule: prime squared, prime <10 → 2,3,5,7 → 4; (2) if you don't know the rule: trial and error 1…9, spot the pattern (4 = 2², 9 = 3²) | solve-q-397 (1<a<200 → 6) | SAME (both methods; English adds the "16 is a square but not of a prime" check and the "only one-digit primes" trap) |
| 12 | 20 שאלות תרגול עצמי · 20 practice questions | 14765 | — | q-403 … q-422 (20) + alg-extra ×2 + q-r26-t14-07/10/12/15 | SAME (all 20 kept) |

**Count by row (26 rows):** SAME 26 · CHANGED 0 · PARTIAL 0 · MISSING 0.
(Two small remarks are not said in English, both without teaching content: 3b's "the biggest divisor of 20 is 20" opener and
4g's "this is the most important lesson".)

### Count by video (her units)

| Unit | Match |
|---|---|
| Intro lesson (1a-1e, incl. 2 examples) | SAME |
| Factors lesson (2a-2d, incl. 1 example) | SAME |
| Greatest divisor lesson (3a-3c, 2 examples) | SAME (now taught inside q-389 / q-390) |
| Break and build lesson (4a-4g, 5 examples) | SAME (now taught inside q-398 … q-402) |
| Advanced Q1-Q7 (5-11) | SAME (7) |
| 20 practice questions | SAME |

**By video: SAME 12 · CHANGED 0 · PARTIAL 0 · MISSING 0** (12 units: 4 lessons, 7 questions, the practice set).

---

## 2. English → Hebrew (added in English)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| primes slide 2 (part) | Odd sum / odd difference of two primes → one is 2 (moved up from her advanced Q1) | her Q1 (391) | yes |
| primes-2 slide 1 | Testing a bigger number with the primes up to its root (91, 89); the "fake primes" 51, 57, 87, 91, 119 | none | yes (re-read pending) |
| primes-3 slides 1-2 | The factor tree (180) and "each prime enough times" (8 ∤ 180); unpack 6², 10² | her 60 example, her Q2c | yes |
| prime-tools slides 2-3 | Number of divisors: add 1 to each exponent and multiply (44, 3³·5², the 56 = 4·14 trap) | none | yes (re-read pending) |
| solve-q-389 slides 1-2, solve-q-390 slides 1-2 | GCD in numbers (172/112); LCM; GCD × LCM = product | none (her "cancel the shared prime" is the seed) | yes (re-read pending) |
| 2nd methods in q-387, q-388, q-389, q-393, q-396, q-398, q-400, q-401, q-402 | Plugging in the answers / dividing / parity / estimating | none | yes |
| solve-q-r26-t14-01 | Which is prime (91, 119, 113, 133): root test, digit-sum test for 3, "never forget 7", counting by sevens | none | yes |
| r26-t14-more-tools | Perfect squares: every exponent even; the smallest k with 45k a square | none | yes (re-read pending) |
| solve-q-r26-t14-03 | 2^a·3^b = 108: unique factorization, match exponents, dividing down | none | yes (re-read pending) |
| r26-t14-summary | Summary page | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | Guaranteed divisor opener: "the biggest divisor of a known number is the number itself (20, 300), so we look for the biggest one we *know* is there" | solve-q-390 slide 0, 1-2 sentences | yes (done) | OPTIONAL. A nice way into the idea, but the English "it must divide even the smallest number that fits" (slide 1) does the same job |
| 2 | "Break and build is the most important lesson in the topic" | — | — | NOT NEEDED (no teaching content; that lesson no longer exists as a video) |
| 3 | Her which-way verdicts (Q6 "standard is recommended", Q8 "if you can do it without plugging in, great") | — | — | NOT NEEDED (R35) |

**RESTORE list: none.** Every method, named trick and warning she gives in topic 14 is in the English, and every one still
works with the English numbers. Nothing in the English contradicts her.
