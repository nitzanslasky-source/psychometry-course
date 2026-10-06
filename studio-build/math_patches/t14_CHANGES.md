# Topic 14 — Prime Numbers: changes

Patch: `math_patches/t14.py`. Check: `python3 math_check.py 14` shows 0 problems, 0 warnings and 0 layout problems (70 slides checked).

## Summary
- Questions: 41 rewritten, 15 added (4 guided with solution videos and 11 practice), 3 removed.
  The topic had 44 questions (17 guided and 27 practice). It now has 56 (21 guided and 35 practice).
- Order: the GCD question (old Q4) and the "greatest guaranteed divisor" question (old Q5) now come right after the "Factor Tools" lesson and its card. Before, they came before these ideas were taught.
- The guided questions are renumbered automatically in course order: 4 in theory A, 7 in theory B, and 10 in the advanced section.
- Lesson "Prime Numbers": 5 slides changed, 1 slide added ("Is it prime?").
- Lesson "Factor Tools": 7 slides changed, 1 slide added ("GCD vs LCM", a table).
- New lesson video: "More Factor Tools" (6 slides, about 3.3 minutes). It is the first item of the advanced section.
- New solution videos: 4. Changed solution videos: 6 (old Q4, Q5, Q6, Q11, Q12 and Q15).
- Memory cards: 2 updated, 1 new ("More factor tools").
- Figures: none in this topic.

## 1. Wrong or misleading teaching (fixed)
- **"Prime Numbers", slide 2:** deleted "The primes are the small numbers you never meet as an answer inside the times table." This was false.
- **GCD and LCM rule:** the vague words "offset it", "count it once" and "shared ones once" are gone everywhere. That includes lesson slide 3, the recap, the card, and the old Q5 video. The rule now reads:
  - **GCD:** each shared prime, at its LOWER power.
  - **LCM:** every prime, at its HIGHER power.
  - The official names (greatest common divisor, least common multiple) are said and written. The course also says that the "greatest guaranteed divisor" is the LCM.
- **Recap mismatch:** the teacher used to underline "counted once", but the board said something else. The recap is rewritten, and the teacher now underlines "LOWER" and "HIGHER".
- **Old Q4 video:** it used "least common multiple" before the course taught it. It now comes after the lesson, and it says "lower power" and "the trap is the higher power: that's the LCM".
- **Solution texts fixed:**
  - q-420: removed "it is always integers". The question itself was removed as a duplicate.
  - q-422: the confusing "product … divided by nothing" sentence is gone.
  - extra-t14-4-2: now "take each prime at its higher power: $2^2\cdot3^2=36$".
  - extra-t14-4-1: now shows the GCD with the primes.
  - extra-t14-4-4: now uses a taught idea. The divisors of a prime $p$ are only $1$ and $p$, and $p$ leaves remainder $1$ in $2p+1$. The "divides the difference" idea is no longer needed.

## 2. Methods added
**Lesson "Prime Numbers"**
- **Slide 3 "0, 1 and 2":**
  - $0$, $1$ and negative numbers are not prime.
  - New board line: "Odd sum or difference of two primes → one is 2". It also explains odd + odd = even. This parity idea is used in old Q11, q-412 and q-415, and T16 comes later.
- **New slide 5 "Is it prime?":**
  - The √n test, with 91 as the example.
  - The digit-sum test for 3 (T15 comes later).
  - A list of fake primes: 51, 57, 87, 91, 119.
- **Recap:** it now has the parity line and the √n line, and it says "Four questions next".
- **Card:**
  - The primes table now goes up to 60.
  - New facts: 0/1/negatives, parity, √n.
  - New table of fake primes (51, 57, 87, 91, 119, 133).
  - New tip: the digit-sum test for 3.

**Lesson "Factor Tools"**
- **Slide 2 (GCD):** the lower-power rule, shown step by step for 72 and 90.
- **Slide 3 (LCM):** the higher-power rule, shown step by step for 72 and 90.
- **New slide 4 "GCD vs LCM":**
  - A table of 72 and 90, one prime per row, with the lower-power and higher-power columns.
  - GCD × LCM = a × b, checked: 18 · 360 = 72 · 90 = 6480.
  - The trap: multiplying the two numbers.
- **Break & build:** a named method for letter questions (old Q14). "Letters as primes? Plug in 2, 3, 5, 7, then check every choice."
- **Symmetric divisors:** now uses the general rule. An odd number of divisors means a perfect square (36 has 9 divisors). "Exactly 3 divisors → prime squared" is the common special case.
- **Recap and card:** rewritten to match. The card has 6 rows and 3 tips, including the "multiply them" trap and plugging in small primes. The recap says "Then seven questions".

**New lesson "More Factor Tools"** (advanced section, before the old advanced questions)
1. Perfect squares and cubes by exponents: 18k a square → k = 2; 18k a cube → k = 12.
2. Prime equations by unique factorization: 2ᵃ·3ᵇ = 72; p²q = 50 (with the "which one is squared" trap).
3. Zeros at the end: pairs of 2 and 5. For example, 2⁵·5³·7 = 28,000.
4. A prime that divides a product divides one of the factors. The counterexample for non-primes: 6 divides 4·9 but neither 4 nor 9. Old Q15 needs this.
5. Recap. A new card, "More factor tools", comes right after the lesson. Its tips include "never true is also not necessarily true".

**Old Q15 video:** new closing lines. "Statement four is NEVER true. Never true is also 'not necessarily true'."

**New guided questions**, each with a solution video:

| New # | id | Question | Answer | Method |
|---|---|---|---|---|
| Q4 | q-r26-t14-01 | Which is prime: 91, 119, 113, 133? | 113 | √n test; all 3 fakes divide by 7 |
| Q12 | q-r26-t14-02 | smallest k with 24k a perfect cube | 9 | exponents divide by 3 (traps: 6 gives a square, 72 is not the smallest) |
| Q13 | q-r26-t14-03 | 2ᵃ·3ᵇ = 108, a − b = ? | −1 | break and match (trap: swapping gives 1) |
| Q14 | q-r26-t14-04 | zeros at the end of 20⁴·15³ | 7 | pairs of 2 and 5 (traps: 4, 8) |

**Strong-student tricks, taught explicitly:**
- Plug in the smallest primes: Break & build slide, and the card.
- Try the choices: already in old Q12 and Q14, and used in the new Q4 video.
- GCD × LCM as a shortcut and a check.
- The √n test and fake primes.
- Parity of two primes.

## 3. Text (all 41 existing questions)
- Every stem, choice and solution is now in TeX. No ":" is used for division: q-387, q-396 "280:35", q-408, q-417 "n:d" and q-421 are fixed. The extras' plain-text choices are now TeX.
- Board slide 6 of "Prime Numbers": "20 : 4 = 5" is now "20 ÷ 4 = 5", and the same for 30 ÷ 6. The spacing in the "Counting divisors" draw notes is fixed. The board "9: 1, 3, 9" is now "Divisors of 9: 1, 3, 9".
- **Stacked conditions:**
  - q-389 (x and y), q-393 (a < b and the equation) and q-399 (xy = 36 and A = |x − y|) use `cases`.
  - q-392, q-394, q-395, q-397, q-402, q-409 and q-414 show one given per line.
- **Rewording:**
  - q-396: "The prime factors of a are 2 and 5 only" is now "a has exactly two prime factors: 2 and 5". It now asks for "the smallest possible value of $\frac{a\cdot b}{35}$".
  - q-401: "What is correct to say about y?" is now "Which of the following is necessarily true?"
  - q-400: now says "each number at most once".
  - q-407: adds "x > 44".
  - q-415: the needless "1 < p" is removed.
  - The extras now use NITE-style stems ("What is the GCD of …?").
- The word-only extra solutions now show the numbers.
- The solutions use the taught methods: lower/higher power, √n, pairs of divisors, and parity of two primes.
- Every mid-sentence "so" is now "therefore".
- The solution-video titles and preloaded-question notes match the new stems.

## 4. Figures
None in this topic.

## 5. Practice
**Removed (near-duplicates):**
- q-416 ("t² is prime", the same as guided Q10)
- q-420 (the third "exactly 3 divisors" item)
- q-410 (GCD with letter primes, the same as guided Q5)

**Added:**

| id | Question | Answer |
|---|---|---|
| q-r26-t14-05 | how many primes between 80 and 100 | 3 (83, 89, 97) |
| q-r26-t14-06 | sum of the primes between 50 and 60 | 112 (fakes 51, 57 give 163, 169, 220) |
| q-r26-t14-07 | 1 < n < 120, not divisible by 2, 3, 5, 7 → necessarily | n is prime (exam-hard) |
| q-r26-t14-08 | GCD 6, LCM 180, one number 36 → the other | 30 |
| q-r26-t14-09 | LCM of p³q and p²q⁴ | p³q⁴ |
| q-r26-t14-10 | smallest k with 2³·3⁴·5·k a square | 10 |
| q-r26-t14-11 | smallest m with 2⁴·3²·m a cube | 12 |
| q-r26-t14-12 | p²q = 75, p + q | 8 |
| q-r26-t14-13 | 6ˣ·5ʸ = 1080, x + y | 4 (exam-hard) |
| q-r26-t14-14 | zeros at the end of 1·2·…·20 | 4 (exam-hard) |
| q-r26-t14-15 | 14 divides ab → necessarily | 7 divides a or b (exam-hard) |

**Order:** the practice runs from easy to hard. The easy extras come first. The exam-hard items come last: q-407, 13, 14, 15, q-415, q-417, q-422, 07, q-408 and q-421. That makes 10 exam-level items.

Every new or changed answer was checked by hand and by brute force.

## Not done / for the teacher to decide
- **Parity (T16) and the digit-sum test for 3 (T15)** are taught here in one or two lines each, because this topic needs them first. If T15/T16 move before T14 (PLAN.md suggests T16 before T15), these lines can stay as reminders.
- **Recording length:**
  - "Prime Numbers": about 6.3 minutes (it was 4.7).
  - "Factor Tools": about 5.2 minutes (it was 3.4).
  - The new "More Factor Tools": about 3.3 minutes.
- **The q-389 stem on the slide** is drawn in a smaller font, because the stacked `cases` block makes it tall. It is readable, but check it in the recording.
- **Module numbers:**
  - The moved Q4 and Q5 solution videos now belong to the "Factor Questions" group (module 42).
  - The new lesson shares module 43 with the "Advanced Primes" group, because the API has no way to create a new module number.
- **"Primes near the target" strip (2 to 60):** added to the memory card as a table, not as a separate slide.

## Pass 2 (teacher-approved remove/restore plan, 2026-09-27)

**Removed** (not on the real exam and not in the original course: zeros at the end of a number, perfect cubes, finding a number from its GCD and LCM):
- Video "More Factor Tools": slide "Zeros at the end", its sidebar label and its Recap line. The slide "Squares & cubes" lost its cube lines and is now called "Perfect squares". The title and recap now say "three tools".
- Guided q-r26-t14-02 (24k a perfect cube) and q-r26-t14-04 (zeros of 20⁴·15³), with their solution videos. The advanced guided questions are renumbered (the prime-equation question is now Question 12, q-391 is Question 13).
- Practice q-r26-t14-08 (GCD 6, LCM 180 → the other number), q-r26-t14-11 (cube), q-r26-t14-14 (zeros of 20!).
- Card "More factor tools": rows "Perfect cube" and "Zeros at the end"; intro now "Three tools".

**Kept:** q-r26-t14-10 (smallest k so that 2³·3⁴·5·k is a square).

**Restored** (3 original questions, text clean-up only: TeX, stacked givens, full numeric solutions; same choices and key):
- q-416 (t > 1, t² prime → t is not an integer), q-420 (exactly three divisors → √m is prime), q-410 (GCD of p²q³r and p³qr² = p²qr).
- They are back in the independent practice at matching difficulty (q-410 with the GCD/LCM items, q-416 and q-420 next to q-417).
- The recap lines "Know the primes up to 40 — and 97" and "Divides by every combination of its prime factors", the two `mem-primes` tips and the `mem-factor-tools` tip ("Divides by 2 and 5 → by 10 …") that the plan lists were already present in the pass-1 patch, so nothing more was needed.

**New: summary video** `r26-t14-summary` "Prime Numbers — Summary", at the end of the advanced section, right before the independent practice (about 2.6 minutes).
Slides: Summary · What a prime is · Two primes, odd result · Is it prime? · Break it down · GCD and LCM · Counting divisors · Squares and equations · A prime in a product · Before you practice.
It only repeats what the three lessons teach. The last slide lists the checks (broke it into primes? really prime - tried up to the root and 7? odd sum → one prime is 2? GCD or LCM - lower or higher power?) and the traps (calling 1 a prime, forgetting 2, multiplying instead of taking the LCM).

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). The lessons were teaching each question's idea, and then the question video taught it again. Lessons are now short intros; every idea is still taught, once, inside the question that uses it. Nothing in topic 14 is recorded. "Prime Numbers" (the first lesson) is unchanged.
- **`prime-tools` "Factor Tools"**: 5.2 → 1.5 min. Kept: the title (now "In this section: questions about the factors of a number…"), "Break & build" (the frame of the section, with "letters as primes? plug in 2, 3, 5, 7") and "Counting divisors" (no question video teaches it; the practice uses it). Sidebar: Break & build · Counting divisors.
  - Cut "GCD" → taught in Q5 `solve-q-389` (lower power). Added there: "The GCD is the biggest number that divides both."
  - Cut "LCM" → taught in Q6 `solve-q-390` (higher power, "multiply them? no"). Title line now gives the official name "least common multiple — LCM".
  - Cut "GCD vs LCM" → the GCD · LCM = a · b fact moved to Q6 as one line + board item ("GCD · LCM = a · b: 4 · 24 = 8 · 12 = 96"). The trap (just multiplying) is already in Q5 and Q6.
  - Cut "Symmetric divisors" → taught in Q11 `solve-q-402` (pairs, the middle divisor). Added there: "In general: an odd number of divisors means a perfect square" + board item. "Remember the symmetric divisors?" reworded.
  - Cut "Recap"; its closing line moved to the last kept slide.
- **`r26-t14-more-tools` "More Factor Tools"**: 2.4 → 1.1 min. Kept: "Perfect squares" (no question video teaches it). Its example 18k was exactly practice question `alg-extra-unit-t14-4-6` → now 12k (k = 3, 36 = 6²); same change on card `mem-r26-t14-more-tools`.
  - Cut "Prime equations" → taught in Q12 `solve-q-r26-t14-03` (one way to break into primes, match the exponents; swap trap).
  - Cut "A prime in a product" → Q17 `solve-q-395` now says it as a rule, at the moment it is used (+ board item): a prime can't be split between factors; 15 isn't prime, so its 3 and 5 may come from different numbers.
  - Cut "Recap".
- Cards unchanged (except the 12k example). Summary `r26-t14-summary` not affected.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has new numbers, letters or a slightly changed story. The idea, the trap, the difficulty and the methods stay the same, and every guided solution video is rewritten to match (board, speech, draw cues, video title). Nothing in Topic 14 is recorded (checked ~/Documents/Course.recordings), so nothing had to be kept as it was. Function `renumber(M)` in t14.py runs last.

**Counts:** 17 guided questions renumbered (q-386 … q-402) with their 17 solution videos rewritten; 20 practice questions renumbered (q-403 … q-422); lesson examples renumbered: 6 slides of "Prime Numbers" (13/14, primes 30–40, 20 ÷ 4 and 30 ÷ 6, 12 = 2·2·3, the 126 factor tree, 126 with 18/12) and 1 slide of "Factor Tools" (2³·5² → 12 divisors), plus the Hebrew examples on the cards `mem-primes` and `mem-factor-tools` (72 and 90 → 45 and 75; 8 · 12 trap → 6 · 10; "2 and 5 / 2 and 6" → "3 and 7 / 3 and 9"; divisors of 9 → of 4). Practice: 35 → 26.

**Kept on purpose:** the English-only questions q-r26-t14-01 (113 is prime) and q-r26-t14-03 (2ᵃ·3ᵇ = 108), the English lesson slides (root test with 91, "25 = 2 + 23", perfect squares 12k) and the summary video are not Hebrew-derived and stay. Choice positions were moved in most questions.

**Order:** theory A is now easy → hard in the order the lesson teaches: q-387 (trial and error), q-r26-t14-01 (root test), q-388 (missing prime), q-386 (number line). Advanced: q-396 (minimum question) now comes before the two hard letter questions q-394 and q-395. Question numbers, sidebars and spoken "Question N" are renumbered by the build.

**Practice clean-up:** removed the copy `alg-extra-unit-t14-4-5` (which is prime: 29, 21, 27, 33 — the same as guided Q2); extra warm-ups kept: GCD of 36 and 54, LCM of 12 and 18 (removed 4-3 counting divisors, 4-4 GCD of p and 2p+1, 4-6 18k square, 4-7 pq = 91); September items removed where the Hebrew practice has the type: q-r26-t14-05 (primes 80–100), -06 (sum of primes 50–60), -09 (LCM with letters), -13 (6ˣ·5ʸ = 1080, the same type as -12, which stays). Kept September items (types the Hebrew practice lacks): -07 (root test), -10 (perfect square), -12 (prime equation), -15 (a prime in a product). **For the teacher:** -13 also practises a type the Hebrew lacks; it was cut only to stay near the target of 25 (26 now). Put it back if you want it.

**Checks:** every answer was brute-forced in Python (exactly one correct choice; trap still among the choices; every method in each video works with the new numbers). `math_check.py 14` → 0 problems, 0 warnings, 0 layout problems. All changed videos rendered and looked at. Duplicate check over topics 1–14: no question equals another question or a lesson / card example.

| id | old (Hebrew numbers) | new | answer |
|---|---|---|---|
| q-387 (G) | x prime, x⁵ two-digit, 7x | x prime, x⁶ two-digit, 9x | 18 (x = 2) |
| q-388 (G) | x = 3·2³·10², not a divisor: 15, 20, 30, 21 | x = 5·3²·6², not a divisor: 12, 35, 45, 18 | 35 |
| q-386 (G) | x < 20 < y, 2 primes each side; 14·30 | x < 40 < y; x = 30 forced (29 prime), y = 44–46 | 1320 (traps 1276 = 29·44, 1200, 1380 = largest) |
| q-389 (G) | GCD of a²bc⁴d and a³c²d² | GCD of p³q²s and pq⁵rs² | pq²s (LCM trap = choice 2) |
| q-390 (G) | divisible by 8 and 12 → 24 (trap 96) | divisible by 10 and 25 | 50 (trap 250 = product; GCD·LCM 5·50 = 250) |
| q-398 (G) | 3-digit number, digits 1, 2, 3; not 10 | lock code, digits 1, 3, 5: 45, 30, 25, 15 | 30 |
| q-399 (G) | xy = 36, max A − min A = 16 (trap 11) | xy = 100 | 48 (trap 33 = forgetting 10·10) |
| q-400 (G) | products of 2, 3, 7 → 83 (trap 41) | Dan's cards 2, 5, 7 | 129 (trap 59) |
| q-401 (G) | y² prime | m² prime, new choice order; plug in m² = 5, 2 | m is not an integer |
| q-402 (G) | n with 3 divisors, B = √n; example 49 | k with 3 divisors, C = √k; example 25 | 2 |
| q-391 (G) | a+b cannot be 25, 27, 33, 45 → 27 | p+q: 15, 31, 51, 43 | 51 (= 2 + 49) |
| q-392 (G) | 10, 15, 7 / 22, 15, 30 → 5·11 = 55 | 14, 21, 5 / 26, 21, 42 | 7·13 = 91 (both methods) |
| q-393 (G) | ab + 2a = 36, a < b; not 15 | ab + 4a = 48, a < b: 45, 15, 17, 12 | 17 (22 also possible, not a choice) |
| q-396 (G) | a from {2, 5}, b from {2, 7}, b < a, ab/35 = 8 (trap 4) | a from {3, 5}, b from {3, 7} | 27 = 45·21/35 (trap 9 ignores b < a) |
| q-394 (G) | y = a^d·b^c, a<b<c<d → a^c·b^a | z = p^r·q^s, p<q<r<s | p^q·q^r (plug in 2, 3, 5, 7: z = 2⁵·3⁷) |
| q-395 (G) | abc divisible by 15, x², answer 4 | abc divisible by 35, x³, statements reordered | (2) — never true |
| q-397 (G) | 1 < a < 150, 3 divisors → 5 | 1 < a < 200 | 6 (4, 9, 25, 49, 121, 169) |
| q-403 | most divisors: 13, 66, 55, 87 | 57, 17, 70, 65 | 70 (8 divisors) |
| q-404 | primes < 20, max a − b = 17 | primes < 30 | 27 (trap 26 forgets 2) |
| q-405 | calculator ×2, ×7: not 42 | machine ×2, ×5: 50, 30, 80, 40 | 30 |
| q-406 | greatest 1-digit + greatest 2-digit prime = 104 | greatest − smallest two-digit prime | 86 |
| q-407 | x > 44, 2 primes; not 60 | x > 74: 86, 90, 84, 88 | 90 |
| q-408 | a·b²·c³ cannot be 24, 21, 40, 72 → 21 | k·m²·n³: 36, 56, 54, 15 | 15 |
| q-409 | odd 1-digit prime × 2-digit prime < 30 → 33–203 | × 2-digit prime > 80 | 249 ≤ x ≤ 679 (traps 166 uses 2, 873 uses 9) |
| q-410 | GCD of p²q³r, p³qr² | GCD of K = a³b²c⁴, L = a²b⁵c | a²b²c (LCM trap a³b⁵c⁴) |
| q-411 | x = 2²·5³: 75, 8, 50, 200 | x = 3²·5³: 45, 27, 675, 30 | 45 |
| q-412 | difference cannot be 21, 9, 15, 23 → 23 | m, n: 17, 33, 27, 39 | 33 (35 not prime) |
| q-413 | "interesting": 11, 5, 4, 6 → 4 | "lucky": 12, 9, 6, 18 | 9 (2+3+5+7 = 17) |
| q-414 | ab = 75, a − b cannot be 15 | ab = 98: 47, 7, 97, 14 | 14 |
| q-415 | p < q, p+q prime → p = 2 | s < r, r+s prime; choices r+s = 19, s+5 < r | s = 2 |
| q-416 | t > 1, t² prime; example √97 | w > 1, w² prime; example √89 | w is not an integer |
| q-417 | n has an odd number of divisors; example 16 | k; example 4 | √k is an integer |
| q-418 | Dana's poem, 20 words → 37 | Maya reads 30 pages, 5 days | 43 |
| q-419 | n/18 in lowest terms → 6 | n/20 | 8 (traps 7 forgets 1, 10 = odd numbers only) |
| q-420 | m with 3 divisors, √m; example 9 | t; example 4 | √t is prime |
| q-421 | n² divisor > 2n → 6 | divisor > 3n: 9, 6, 10, 8 | 8 (6 = the old answer is the trap) |
| q-422 | Alan/Beth, 4 and 6: 24 vs 12 | Tom/Rina, 6 and 9: 54 vs 18 | Only Rina |

## 2026-10-06 review
Independent check of the renumber pass (17 guided + 20 practice, 17 solution videos, lessons "Prime Numbers" / "Factor Tools", cards mem-primes / mem-factor-tools, practice removals). Every key brute-forced in Python (exactly one correct choice, trap still a choice); every video step redone with the new numbers and checked for old numbers (none left); duplicates checked against topics 1–16 questions, lessons and cards (none). Nothing in topic 14 is recorded. Rendered solve-q-386, -392, -395.
- q-406: the renumber had changed the type (Hebrew: greatest ONE-digit prime 7, not 9, together with greatest two-digit prime 97, not 99; the new version dropped the one-digit fact). Now: the difference between the greatest two-digit prime and the greatest one-digit prime, $97-7=90$. Choices 88 (9 taken as prime), 92 (99 taken as prime), 90, 86 · key 3.
- q-409: the condition "two-digit prime smaller than 30" had become "greater than 80" (a different kind of condition, and harder primes/products). Back to "smaller than": $b$ a two-digit prime smaller than $40$ → $33\le x\le259$ ($3\cdot11$, $7\cdot37$). Choices $22\le x\le259$ (uses 2) / $33\le x\le259$ / $3\le x\le37$ / $33\le x\le333$ (uses 9) · key 2.
- Checked and kept: q-392 (14, 21, 5 / 26, 21, 42 → 7·13 = 91; same "exactly two / exactly one" kind, both methods work), q-395 (35 instead of 15, x³ instead of x² — same "no new prime" message; statement order changed only), q-386 (mirror image: now x is forced and y has three options — same reasoning on the number line), q-421 (> 3n → 8; 6, the old answer, is a trap).
`python3 math_check.py 14 32` → 0 problems, 0 warnings, 0 layout.
- (review follow-up) q-395: back to the Hebrew x² (with 35): statement (2) "the number of different prime divisors of $x^2$ is greater than that of $x$" — never true, key still 2. Explanation ($35^2=1225=5^2\cdot7^2$) and video (board "35 = 5·7 → 35² = 5²·7²", "Square x, and the same primes just appear twice as often") updated. Rendered.
- q-r26-t14-13 ($6^x\cdot5^y=1080$) stays cut: its type (break into primes, match exponents) is the guided q-r26-t14-03 ($2^a\cdot3^b=108$), and practice keeps q-r26-t14-12 ($p^2q=75$).
`python3 math_check.py 14 32` → 0 / 0 / 0.
